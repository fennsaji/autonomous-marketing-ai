"""
Prometheus metrics endpoint for observability.
"""
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.core.metrics import update_connection_pool_metrics
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/metrics")
async def get_metrics():
    """
    Prometheus metrics endpoint.
    Returns metrics in Prometheus exposition format.
    """
    try:
        # Update connection pool metrics before serving
        update_connection_pool_metrics()
        
        # Generate Prometheus metrics
        metrics_data = generate_latest()
        
        return Response(
            content=metrics_data,
            media_type=CONTENT_TYPE_LATEST
        )
        
    except Exception as e:
        logger.error(f"Failed to generate metrics: {e}")
        return Response(
            content=f"# Error generating metrics: {e}\n",
            media_type=CONTENT_TYPE_LATEST,
            status_code=500
        )


@router.get("/metrics/health")
async def get_health_metrics():
    """
    Get health-specific metrics in JSON format.
    Useful for debugging and dashboards.
    """
    try:
        from app.core.circuit_breaker import health_check_circuit_breaker, database_circuit_breaker
        from app.core.metrics import (
            health_checks_total, 
            db_connections_total,
            db_queries_total,
            db_retry_attempts_total
        )
        
        # Update connection pool metrics
        update_connection_pool_metrics()
        
        # Get metric values using proper Counter collection method
        health_check_samples = list(health_checks_total.collect())[0].samples
        db_connection_samples = list(db_connections_total.collect())[0].samples
        db_query_samples = list(db_queries_total.collect())[0].samples
        db_retry_samples = list(db_retry_attempts_total.collect())[0].samples
        
        return {
            "health_checks": {
                "samples": [{"name": s.name, "labels": s.labels, "value": s.value} for s in health_check_samples],
                "total_calls": sum(s.value for s in health_check_samples)
            },
            "database": {
                "connection_samples": [{"name": s.name, "labels": s.labels, "value": s.value} for s in db_connection_samples],
                "query_samples": [{"name": s.name, "labels": s.labels, "value": s.value} for s in db_query_samples],
                "retry_samples": [{"name": s.name, "labels": s.labels, "value": s.value} for s in db_retry_samples],
                "total_connections": sum(s.value for s in db_connection_samples),
                "total_queries": sum(s.value for s in db_query_samples),
                "total_retries": sum(s.value for s in db_retry_samples)
            },
            "circuit_breakers": {
                "health_check": health_check_circuit_breaker.get_stats(),
                "database": database_circuit_breaker.get_stats(),
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get health metrics: {e}")
        return {"error": f"Failed to get health metrics: {e}"}