from Monitoring import Monitor


monitor = Monitor(temperature_limit=62, maintenance_period=180)
monitor.clean_log_file()

monitor.monitor_graphic_cards()
