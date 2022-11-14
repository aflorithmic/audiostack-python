
class AudioForm():
    
    # create a new stack
    # 
    def __init__(self, projectName: str, moduleName: str, scriptName: str) -> None:
        pass    
    
    # loads from remote
    def retrive():
        pass
    
    # loads from remote
    def upload():
        pass
        
    
    # adds a script to this stack
    def add_script():
        pass
    
    # configure speech
    def add_speech_request():
        pass
    
    def add_production_request():
        pass
    
    def add_delivery_endpoints():
        pass
    
    # stack
    def build_stack():
        pass
    
    def generate():
        pass
    
    
    def list():
        pass
    
    def delete():
        pass
    
stack = AudioForm(projectName="helloworld", moduleName="x", scriptName="testing")

# do we put scriptName here?
stack.add_script(scriptText="hello timo!")

# generate a speech request with joanna and one with liam
stack.add_speech_request(voice="Joanna")
stack.add_speech_request(voice="Liam")

# create a production request that uses hotwheels sound template
stack.add_production_request(soundTemplate="hotwheels")

#deliver these to soundcloud, julep etc
stack.add_delivery_endpoints(connector="soundcloud...")

# run the stack
stack.generate()

# list the results
stack.list()
# -> scripts=[], speechFiles=["Liam..", "joanna"], productionFiles=["128123", "1251261"]

# not sure about these two
stack.upload()
stack.delete()
