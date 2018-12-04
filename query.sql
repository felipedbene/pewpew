SELECT 
  events.time_received, events.threatid,device_name,srcloc
FROM 
  public.events
ORDER BY
  events.time_received DESC limit 50;