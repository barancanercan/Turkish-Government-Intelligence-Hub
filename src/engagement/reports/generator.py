"""
Report Generator
Create comparison reports in PDF/HTML format
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportTemplate:
    """
    Report template for party comparisons.
    """
    
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1a1a2e; color: white; padding: 30px; text-align: center; }}
        .meta {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
        .party {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
        .party-name {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
        .party-content {{ line-height: 1.6; }}
        .comparison-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .comparison-table th, .comparison-table td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
        .comparison-table th {{ background: #f5f5f5; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    <div class="meta">
        <p>Tarih: {date}</p>
        <p>Kaynak: MIZAN-AI Political Analysis</p>
    </div>
    
    {content}
    
    <div class="footer">
        <p>Bu rapor MIZAN-AI tarafindan otomatik olarak olusturulmustur.</p>
        <p>Rapor olusturma tarihi: {generated_at}</p>
    </div>
</body>
</html>
"""
    
    def generate_comparison_report(
        self,
        topic: str,
        parties: Dict[str, str],
        sources: List[str],
    ) -> str:
        """
        Generate a comparison report.
        
        Args:
            topic: Comparison topic
            parties: Dict of party name -> position
            sources: List of sources
            
        Returns:
            HTML report string
        """
        content_parts = [f'<h2>Konu: {topic}</h2>']
        
        content_parts.append('<table class="comparison-table">')
        content_parts.append('<tr><th>Parti</th><th>Pozisyon</th></tr>')
        
        for party, position in parties.items():
            content_parts.append(f'<tr><td><strong>{party}</strong></td><td>{position}</td></tr>')
        
        content_parts.append('</table>')
        
        if sources:
            content_parts.append('<h3>Kaynaklar</h3>')
            content_parts.append('<ul>')
            for source in sources:
                content_parts.append(f'<li>{source}</li>')
            content_parts.append('</ul>')
        
        return self.template.format(
            title=f"Karsilastirmali Rapor: {topic}",
            topic=topic,
            content="\n".join(content_parts),
            date=datetime.now().strftime("%d %B %Y"),
            generated_at=datetime.now().strftime("%d %B %Y %H:%M"),
        )
    
    def generate_single_party_report(
        self,
        party: str,
        content: str,
        topics: List[str],
    ) -> str:
        """Generate a single party report."""
        
        content_parts = [f'<h2>Parti: {party}</h2>']
        
        content_parts.append(f'<div class="party"><div class="party-content">{content}</div></div>')
        
        content_parts.append('<h3>Tartisilan Konular</h3>')
        content_parts.append('<ul>')
        for topic in topics:
            content_parts.append(f'<li>{topic}</li>')
        content_parts.append('</ul>')
        
        return self.template.format(
            title=f"Parti Raporu: {party}",
            topic=party,
            content="\n".join(content_parts),
            date=datetime.now().strftime("%d %B %Y"),
            generated_at=datetime.now().strftime("%d %B %Y %H:%M"),
        )


class ReportGenerator:
    """
    Report generator with PDF export.
    """
    
    def __init__(self):
        self.template = ReportTemplate()
    
    async def generate_html(
        self,
        report_type: str,
        data: Dict[str, Any],
    ) -> str:
        """Generate HTML report."""
        
        if report_type == "comparison":
            return self.template.generate_comparison_report(
                topic=data.get("topic", ""),
                parties=data.get("parties", {}),
                sources=data.get("sources", []),
            )
        elif report_type == "single":
            return self.template.generate_single_party_report(
                party=data.get("party", ""),
                content=data.get("content", ""),
                topics=data.get("topics", []),
            )
        
        return ""
    
    async def generate_pdf(
        self,
        report_type: str,
        data: Dict[str, Any],
    ) -> Optional[bytes]:
        """
        Generate PDF report.
        
        Args:
            report_type: Type of report
            data: Report data
            
        Returns:
            PDF bytes or None
        """
        try:
            html = await self.generate_html(report_type, data)
            
            try:
                from weasyprint import HTML
                pdf = HTML(string=html).write_pdf()
                return pdf
            except ImportError:
                logger.warning("WeasyPrint not installed, using HTML")
                return html.encode()
                
        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            return None
    
    def generate_share_link(self, report_id: str) -> str:
        """Generate a shareable link for a report."""
        return f"https://mizan-ai.com/reports/{report_id}"


report_generator = ReportGenerator()
