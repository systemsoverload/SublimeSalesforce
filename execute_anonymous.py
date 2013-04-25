import sublime_plugin, subprocess, sublime

class ExecuteAnonymousCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_status('Salesforce - Execute Anonymous', "Anonymous Code Execution.")

        build_properties_path = "{0}/local-build.properties".format(sublime.active_window().folders()[0])
        build_properties_raw = [line.strip() for line in open(build_properties_path)]

        build_properties = {}
        for idx, prop in enumerate(build_properties_raw):
            if prop and not prop.startswith('#'):
                build_properties[prop.split('=')[0].strip()] = prop.split('=')[1].strip()

        print(build_properties.get('sf.username'))
        print(build_properties.get('sf.password'))

        username = build_properties.get('sf.username')
        password = build_properties.get('sf.password')

        loginEnv = '<?xml version="1.0" encoding="utf-8" ?> \
                <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
                        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"> \
                    <env:Body> \
                        <n1:login xmlns:n1="urn:partner.soap.sforce.com"> \
                            <n1:username>{0}</n1:username> \
                            <n1:password>{1}</n1:password> \
                        </n1:login> \
                    </env:Body> \
                </env:Envelope>'.format(username, password)

        loginUrl = 'https://test.salesforce.com/services/Soap/u/27.0'
        proc = subprocess.Popen([
             'curl'
             , loginUrl
             , '-H', 'Content-Type: text/xml; charset=UTF-8'
             , '-H', 'SOAPAction: login'
             , '-d', '{0}'.format(loginEnv)], stdout=subprocess.PIPE)
        (resp, err) = proc.communicate()

        # if resp.find('faultcode'):
        #     print( self.getTagValue(resp, 'faultstring') )

        #XML-Parserless XML parsing
        sessionId = self.getTagValue(resp, 'sessionId')
        serverUrl = self.getTagValue(resp, 'serverUrl')

        sessionId = resp[resp.find('<sessionId>') + 11 : resp.find('</sessionId>')]
        serverUrl = resp[resp.find('<serverUrl>') + 11 : resp.find('</serverUrl>')]

        # Get the selected text
        for region in self.view.sel():
                if not region.empty():
                        codeToExecute = self.view.substr(region)

        executeAnonymousEnv = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:apex="http://soap.sforce.com/2006/08/apex"> \
        <soapenv:Header>\
                <apex:DebuggingHeader>\
                    <apex:debugLevel>Detail</apex:debugLevel>\
                </apex:DebuggingHeader>\
                <apex:SessionHeader>\
                    <apex:sessionId>{0}</apex:sessionId>\
                </apex:SessionHeader>\
        </soapenv:Header>\
        <soapenv:Body>\
                <apex:executeAnonymous>\
                        <apex:String>{1}</apex:String>\
                </apex:executeAnonymous>\
                </soapenv:Body>\
        </soapenv:Envelope>'.format(sessionId,codeToExecute)

        eaProc = subprocess.Popen([
             'curl'
             , serverUrl.replace('/u/','/s/')
             , '-H', 'Content-Type: text/xml; charset=UTF-8'
             , '-H', 'SOAPAction: executeAnonymous'
             , '-d', '{0}'.format(executeAnonymousEnv)], stdout=subprocess.PIPE)
        (eaResp, eaErr) = eaProc.communicate()

        # self.display_results(self.getTagValue(eaResp, 'debugLog'))

        print( self.getTagValue(eaResp, 'debugLog'))


    def getTagValue( self, xml, tagName ):
        '''
                This is embarrassingly ugly, but there is no easy access to an xml parser in ST2 on linux
        '''
        openingTag = '<{0}>'.format(tagName)
        closingTag = '</{0}>'.format(tagName)
        return xml[ xml.find(openingTag) + len(openingTag) : xml.find(closingTag) ]

    def clear(self):
        self.view.erase_status('Salesforce - Execute Anonymous')

    def display_results(self, results):
        panel = self.view.window().get_output_panel("salesforce")

        edit = panel.begin_edit()
        panel.insert(edit, 0, results)
        panel.end_edit(edit)

        self.view.window().run_command("show_panel", {"panel": "output.salesforce"})




