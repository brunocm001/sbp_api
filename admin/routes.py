from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from database import get_db
from models import Order, Payment, SupportTicket, Platform, Service, ServiceType
from utils.auth import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Dashboard principal de l'administration"""
    
    # Statistiques générales
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    completed_orders = db.query(Order).filter(Order.status == "done").count()
    
    # Chiffre d'affaires
    total_revenue = db.query(func.sum(Order.price_total)).scalar() or 0
    monthly_revenue = db.query(func.sum(Order.price_total)).filter(
        Order.created_at >= datetime.now().replace(day=1)
    ).scalar() or 0
    
    # Calcul de la croissance (simulation)
    last_month_revenue = db.query(func.sum(Order.price_total)).filter(
        and_(
            Order.created_at >= (datetime.now().replace(day=1) - timedelta(days=30)),
            Order.created_at < datetime.now().replace(day=1)
        )
    ).scalar() or 0
    
    revenue_growth = 0
    if last_month_revenue > 0:
        revenue_growth = round(((monthly_revenue - last_month_revenue) / last_month_revenue) * 100, 1)
    
    # Tickets support
    total_tickets = db.query(SupportTicket).count()
    open_tickets = db.query(SupportTicket).filter(SupportTicket.status == "open").count()
    
    # Services
    active_services = db.query(Service).filter(Service.is_active == True).count()
    platforms_count = db.query(Platform).filter(Platform.is_active == True).count()
    service_types_count = db.query(ServiceType).filter(ServiceType.is_active == True).count()
    
    # Temps de réponse moyen (simulation)
    avg_response_time = 2.5
    
    # Dernières commandes
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(10).all()
    
    # Derniers tickets
    recent_tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).limit(5).all()
    
    # Données pour les graphiques
    orders_chart_data = []
    orders_chart_categories = []
    
    # Générer des données pour les 6 derniers mois
    for i in range(6):
        date = datetime.now() - timedelta(days=30*i)
        month_start = date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        orders_count = db.query(Order).filter(
            and_(
                Order.created_at >= month_start,
                Order.created_at <= month_end
            )
        ).count()
        
        orders_chart_data.append(orders_count)
        orders_chart_categories.append(date.strftime('%b %Y'))
    
    orders_chart_data.reverse()
    orders_chart_categories.reverse()
    
    # Données pour le graphique des plateformes
    platforms_data = db.query(
        Platform.name,
        func.count(Order.id).label('orders_count')
    ).join(Order, Platform.id == Order.platform_id).group_by(Platform.name).all()
    
    platforms_chart_data = [p.orders_count for p in platforms_data]
    platforms_chart_labels = [p.name for p in platforms_data]
    
    # Préparer les données pour les commandes récentes
    for order in recent_orders:
        order.status_label = {
            "pending": "En attente",
            "in_progress": "En cours", 
            "done": "Terminé",
            "failed": "Échoué"
        }.get(order.status, order.status)
        
        order.status_color = {
            "pending": "warning",
            "in_progress": "info",
            "done": "success", 
            "failed": "danger"
        }.get(order.status, "secondary")
    
    # Préparer les données pour les tickets récents
    for ticket in recent_tickets:
        ticket.status_color = {
            "open": "warning",
            "responded": "info",
            "closed": "success"
        }.get(ticket.status, "secondary")
    
    stats = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_revenue": total_revenue,
        "monthly_revenue": monthly_revenue,
        "revenue_growth": revenue_growth,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "avg_response_time": avg_response_time,
        "active_services": active_services,
        "platforms_count": platforms_count,
        "service_types_count": service_types_count
    }
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "stats": stats,
        "recent_orders": recent_orders,
        "recent_tickets": recent_tickets,
        "orders_chart_data": orders_chart_data,
        "orders_chart_categories": orders_chart_categories,
        "platforms_chart_data": platforms_chart_data,
        "platforms_chart_labels": platforms_chart_labels
    })

@router.get("/stats", response_class=HTMLResponse)
async def admin_stats(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Page de statistiques détaillées"""
    
    # Statistiques par plateforme
    platform_stats = db.query(
        Platform.name,
        func.count(Order.id).label('orders_count'),
        func.sum(Order.price_total).label('total_revenue'),
        func.avg(Order.price_total).label('avg_order_value')
    ).join(Order, Platform.id == Order.platform_id).group_by(Platform.name).all()
    
    # Statistiques par service
    service_stats = db.query(
        Service.name,
        func.count(Order.id).label('orders_count'),
        func.sum(Order.price_total).label('total_revenue')
    ).join(ServiceType, Service.id == ServiceType.service_id).join(Order, ServiceType.id == Order.service_type_id).group_by(Service.name).all()
    
    # Statistiques temporelles
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    orders_today = db.query(Order).filter(func.date(Order.created_at) == today).count()
    orders_week = db.query(Order).filter(Order.created_at >= week_ago).count()
    orders_month = db.query(Order).filter(Order.created_at >= month_ago).count()
    
    revenue_today = db.query(func.sum(Order.price_total)).filter(func.date(Order.created_at) == today).scalar() or 0
    revenue_week = db.query(func.sum(Order.price_total)).filter(Order.created_at >= week_ago).scalar() or 0
    revenue_month = db.query(func.sum(Order.price_total)).filter(Order.created_at >= month_ago).scalar() or 0
    
    return templates.TemplateResponse("admin/stats.html", {
        "request": request,
        "platform_stats": platform_stats,
        "service_stats": service_stats,
        "orders_today": orders_today,
        "orders_week": orders_week,
        "orders_month": orders_month,
        "revenue_today": revenue_today,
        "revenue_week": revenue_week,
        "revenue_month": revenue_month
    }) 