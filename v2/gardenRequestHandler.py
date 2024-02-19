class GardenRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, controls: dict):
        self.controls = controls
    
    def generateHtmlPage(self):
        htmlContent = "<html><head><title>Garden Control</title></head><body>"
        
        # Iterate through controls and append to the HTML content
        for controlName in self.controls:
            control = self.controls[controlName]
            htmlContent += control.toHtmlElement()
    
        # Add global reset button
        htmlContent += "<a href='/global-reset'>Global Reset</a>"
        
        htmlContent += "</body></html>"
        return htmlContent
    
    def handle_request(self, request):
        if request.startswith('/control'):
            params = self.parseUrlParams(request)
            self.handleControlAction(params)
        elif request.startswith('/global-reset'):
            self.handleGlobalReset()
        
        htmlPage: str = generateHtmlPage()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(htmlPage)))
        self.end_headers()
        self.wfile.write(page)
    
    def parseUrlParams(self, url):
        params = {}
        urlParts = url.split('?')
        if len(urlParts) > 1:
            queryString = urlParts[1]
            pairs = queryString.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                params[key] = value
        return params
    
    def handleGlobalReset(self):
        for controlName in self.controls:
            control = self.controls[controlName]
            control.reset()
    
    def handleControlAction(self, params):
        action = params.get('action')
        controlName = params.get('name')
        control = self.controls[controlName]

        if action == 'update':
            control.update(params)
        elif action == 'reset':
            control.reset()
        elif action == 'pause':
            control.disable()
        elif action == 'resume':
            control.enable()
    
    
    
    
    
    
    
    
    
    
    

    
    # update an existing control
    def updateControl(self, params: dict):
        global controls
        global controlLock
        name: str = params['name']
        if name in controls:
            with controlLock:
                control = controls[name]
            type: str = params['type']
            if type == 'CycleTimer':
                onTime: int = int(params['onTime'])
                control.setOnTime(onTime)
                offTime: int = int(params['offTime'])
                control.setOffTime(offTime)
                startDelay: int = int(params['startDelay'])
                control.setStartDelay(startDelay)
                # allow updates to targetList
            else:
                print('unknown control type:', type)
        else:
            print('Invalid control name, not found:', name)
    
