#!/usr/bin/env python3
"""
Health check script that monitors backend errors and posts summaries.
This script is designed to be run periodically by the cron system.
"""

import sys
import os
from datetime import datetime, timedelta

def run_health_check():
    """Run the health check and return a summary."""
    # Import the observability tools
    try:
        from mcp_obs_logs_search import logs_search
        from mcp_obs_logs_error_count import logs_error_count
        from mcp_obs_traces_get import traces_get
        
        # Check for errors in the last 2 minutes
        time_window = "2m"
        
        # Get error count for the Learning Management Service
        error_count = logs_error_count(
            service="Learning Management Service",
            window=time_window
        )
        
        if error_count > 0:
            # Search for recent errors
            error_logs = logs_search(
                query='_stream:{service.name="Learning Management Service"} AND severity:ERROR',
                limit=5,
                since=time_window
            )
            
            if error_logs and len(error_logs) > 0:
                summary = f"⚠️ System Alert: Found {error_count} errors in the last 2 minutes\n"
                
                # Check for trace IDs in the logs and get trace details if available
                trace_found = False
                for log_entry in error_logs[:1]:  # Check first error for trace
                    if hasattr(log_entry, 'trace_id') and log_entry.trace_id:
                        try:
                            trace_details = traces_get(trace_id=log_entry.trace_id)
                            summary += f".Trace details: {trace_details}\n"
                            trace_found = True
                        except Exception as e:
                            summary += f".Could not retrieve trace details: {e}\n"
                
                if not trace_found:
                    summary += ".No trace details available\n"
                    
                return summary
            else:
                return f"⚠️ Found {error_count} errors but couldn't retrieve details\n"
        else:
            return "✅ System looks healthy - no errors detected in the last 2 minutes\n"
    
    except ImportError as e:
        return f"❌ Could not run health check: Missing required modules ({e})\n"
    except Exception as e:
        return f"❌ Error during health check: {e}\n"

if __name__ == "__main__":
    result = run_health_check()
    print(result)