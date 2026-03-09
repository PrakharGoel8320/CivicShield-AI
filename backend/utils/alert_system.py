"""
Alert Notification System
Sends real-time alerts based on prediction results
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

logger = logging.getLogger(__name__)


class AlertSystem:
    """Manages alerts and notifications based on prediction thresholds"""
    
    # Define alert thresholds for different risk levels
    RISK_THRESHOLDS = {
        'flood_risk_level': {'high': 4, 'medium': 3, 'low': 2},
        'aqi_value': {'high': 150, 'medium': 100, 'low': 50},
        'congestion_level': {'high': 4, 'medium': 3, 'low': 2},
        'waterlogging_risk': {'high': 4, 'medium': 3, 'low': 2},
        'crime_incidents': {'high': 5, 'medium': 3, 'low': 1},
        'pothole_severity': {'high': 4, 'medium': 3, 'low': 2},
        'road_damage_level': {'high': 4, 'medium': 3, 'low': 2}
    }
    
    def __init__(
        self,
        alert_log_path: str = "alerts.log",
        enable_email: bool = False,
        enable_webhook: bool = False,
        email_config: Optional[Dict] = None,
        webhook_url: Optional[str] = None
    ):
        self.alert_log_path = Path(alert_log_path)
        self.enable_email = enable_email
        self.enable_webhook = enable_webhook
        self.email_config = email_config or {}
        self.webhook_url = webhook_url
        
        # Setup alert logging
        self.alert_logger = logging.getLogger('alerts')
        self.alert_logger.setLevel(logging.INFO)
        
        # File handler for persistent storage
        file_handler = logging.FileHandler(self.alert_log_path)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.alert_logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('🚨 %(asctime)s - %(message)s')
        )
        self.alert_logger.addHandler(console_handler)
    
    def evaluate_prediction(
        self,
        target_name: str,
        prediction_value: float,
        input_data: Dict[str, Any],
        dataset_name: str = "unknown"
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate if a prediction warrants an alert
        
        Returns:
            Alert dict if threshold exceeded, None otherwise
        """
        # Get thresholds for this target
        thresholds = self.RISK_THRESHOLDS.get(target_name)
        if not thresholds:
            # No defined thresholds - check generic high values
            if prediction_value >= 4:
                severity = 'high'
            elif prediction_value >= 3:
                severity = 'medium'
            else:
                return None
        else:
            # Use defined thresholds
            if prediction_value >= thresholds['high']:
                severity = 'high'
            elif prediction_value >= thresholds['medium']:
                severity = 'medium'
            else:
                return None
        
        # Create alert
        alert = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'target': target_name,
            'predicted_value': prediction_value,
            'dataset': dataset_name,
            'input_data': input_data,
            'message': self._generate_alert_message(target_name, prediction_value, severity)
        }
        
        return alert
    
    def send_alert(self, alert: Dict[str, Any]):
        """Send alert through all enabled channels"""
        
        # 1. Log to file and console
        severity_icon = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        
        icon = severity_icon.get(alert['severity'], '⚠️')
        self.alert_logger.warning(
            f"{icon} {alert['severity'].upper()} ALERT: {alert['message']}"
        )
        self.alert_logger.info(f"   Dataset: {alert['dataset']}")
        self.alert_logger.info(f"   Predicted Value: {alert['predicted_value']:.2f}")
        
        # 2. Send email if enabled
        if self.enable_email and self.email_config:
            try:
                self._send_email_alert(alert)
            except Exception as e:
                logger.error(f"Failed to send email alert: {e}")
        
        # 3. Send webhook if enabled
        if self.enable_webhook and self.webhook_url:
            try:
                self._send_webhook_alert(alert)
            except Exception as e:
                logger.error(f"Failed to send webhook alert: {e}")
    
    def _generate_alert_message(
        self,
        target_name: str,
        prediction_value: float,
        severity: str
    ) -> str:
        """Generate human-readable alert message"""
        
        messages = {
            'flood_risk_level': f"High flood risk detected (Level {prediction_value:.0f}). Prepare evacuation protocols.",
            'aqi_value': f"Poor air quality detected (AQI: {prediction_value:.0f}). Health advisory in effect.",
            'congestion_level': f"Severe traffic congestion (Level {prediction_value:.0f}). Consider alternate routes.",
            'waterlogging_risk': f"Waterlogging risk detected (Level {prediction_value:.0f}). Check drainage systems.",
            'crime_incidents': f"Elevated crime risk ({prediction_value:.0f} incidents predicted). Increase patrols.",
            'pothole_severity': f"Severe potholes detected (Level {prediction_value:.0f}). Immediate repair needed.",
            'road_damage_level': f"Critical road damage (Level {prediction_value:.0f}). Road closure recommended."
        }
        
        return messages.get(
            target_name,
            f"{target_name}: {severity} alert triggered (value: {prediction_value:.2f})"
        )
    
    def _send_email_alert(self, alert: Dict[str, Any]):
        """Send email notification"""
        if not all(k in self.email_config for k in ['smtp_server', 'smtp_port', 'sender', 'recipients']):
            logger.warning("Email config incomplete, skipping email alert")
            return
        
        msg = MIMEMultipart()
        msg['From'] = self.email_config['sender']
        msg['To'] = ', '.join(self.email_config['recipients'])
        msg['Subject'] = f"🚨 {alert['severity'].upper()} Alert: {alert['target']}"
        
        body = f"""
CivicShield AI - Alert Notification

Severity: {alert['severity'].upper()}
Target: {alert['target']}
Predicted Value: {alert['predicted_value']:.2f}
Timestamp: {alert['timestamp']}
Dataset: {alert['dataset']}

Message: {alert['message']}

Input Data:
{json.dumps(alert['input_data'], indent=2)}

---
This is an automated alert from CivicShield AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            if self.email_config.get('use_tls', True):
                server.starttls()
            
            if 'username' in self.email_config and 'password' in self.email_config:
                server.login(self.email_config['username'], self.email_config['password'])
            
            server.send_message(msg)
        
        logger.info(f"✉️ Email alert sent to {len(self.email_config['recipients'])} recipients")
    
    def _send_webhook_alert(self, alert: Dict[str, Any]):
        """Send webhook notification"""
        try:
            response = requests.post(
                self.webhook_url,
                json=alert,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"🌐 Webhook alert sent successfully")
        except requests.RequestException as e:
            logger.error(f"Failed to send webhook: {e}")
    
    def get_recent_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent alerts from log file"""
        alerts = []
        
        if not self.alert_log_path.exists():
            return alerts
        
        try:
            with open(self.alert_log_path, 'r') as f:
                lines = f.readlines()
                
            # Parse last N lines
            for line in lines[-limit:]:
                if 'ALERT' in line:
                    alerts.append({'log': line.strip()})
            
            return alerts
        except Exception as e:
            logger.error(f"Error reading alert log: {e}")
            return []


def create_alert_system(config: Optional[Dict] = None) -> AlertSystem:
    """Factory function to create configured AlertSystem"""
    config = config or {}
    
    return AlertSystem(
        alert_log_path=config.get('alert_log_path', 'alerts.log'),
        enable_email=config.get('enable_email', False),
        enable_webhook=config.get('enable_webhook', False),
        email_config=config.get('email_config'),
        webhook_url=config.get('webhook_url')
    )
