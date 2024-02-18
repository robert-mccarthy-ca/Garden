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
        control = self.controls[control_name]

        if action == 'update':
            # Implement control update logic using attributes from params
            pass
        elif action == 'reset':
            control.reset()
        elif action == 'pause':
            control.pause()
        elif action == 'resume':
            control.resume()
    
    
    
    
    
    
    
    
    
    
    
    def do_GET(self):
        # build our parameters dictionary from the path. 
        #   'name' contains the control name
        #   'type' contains the Controller type
        #   'operation' contains the operation type
        #   the rest are the parameters for the Controller
        parameters: dict = getParametersFromPath(self.path)
        if len(parameters) > 1:
            operation: str = parameters['operation']
            if operation == 'update':
                updateControl(parameters)
            elif operation == 'new':
                createControl(parameters)
            elif operation == 'delete':
                deleteControl(parameters)
            else:
                print('unknown operation:', operation)
                # send error response back
                self.send_response(400)
                return
          
        # build and return the webpage unless we errored out above
        # all valid GET requests to this server return this page
        htmlPage: str = buildHtml()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(htmlPage)))
        self.end_headers()
        self.wfile.write(page)
    
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
    
    def createControl(self, params: dict):
        type: str = params['type']
        if type == 'CycleTimer':
            onTime: int = int(params['onTime'])
            offTime: int = int(params['offTime'])
            startDelay: int = int(params['startDelay'])
            name: str = params['name']
            control: CycleTimer = CycleTimer(name, )
        return None
    
    def deleteControl(self, params: dict):
        return None
    
    def getParametersFromPath(self, path: str) -> dict:
        result: dict = {}
        pathParts: list = path.split('?')
        if len(pathParts) == 1:
            return result
        result['name'] = pathParts[0]
        for queryPair: str in pathParts[1].split('&'):
            queryParts = queryPair.split('=')
            result[queryParts[0]] = queryParts[1]
        return result
    
    def handle_error(self, msg: str):
        do_GET()