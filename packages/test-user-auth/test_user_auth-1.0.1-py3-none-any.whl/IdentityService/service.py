import os 
import json
import pandas as pd 


class IdentityService:
    
    def __init__(self, data_file_name='data_file.json', path_=None):
        # self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.BASE_DIR=os.getcwd()
        if path_==None:
            self.REGISTER_LOG_FILE = os.path.join(self.BASE_DIR, data_file_name)
        else:
            self.REGISTER_LOG_FILE = path_ #user defined path

    def register_log_init(self):
        '''Initiate register logs file 
            if it does not exist
        '''
        if not os.path.isfile(self.REGISTER_LOG_FILE):
            with open(self.REGISTER_LOG_FILE, 'w'):
                pass
            

    def save_to_json(self, path: str, data_frame: pd.DataFrame, overwrite=False):
        '''This method overwrites .json file with 
            newly added user data
        '''
        if overwrite==True:
            old_data=pd.read_json(path)
            old_data['password']=old_data['password'].astype(str) #making sure that password
                                                                  #collumn is str type

            #for the sake of simplicity I've avoided nested json structure
            with open(path, 'w')  as data_file:  
                new_data=old_data.append(data_frame, ignore_index=True)
                results=new_data.to_json(orient='records') #Convert the dataframe to a JSON string
                parsed=json.loads(results) #JSON decoding
                json.dump(parsed, data_file, sort_keys=False, indent=4)
                    
        
    def register(self, username: str, password: str, **properties: dict) -> bool:
        self.register_log_init()
        register_dict=dict()
        register_dict['username']=username
        register_dict['password']=password   
        if self.authenticate(username, password, in_method=True):
            print('User is already registered')
            return False
        elif len(username)<3 or len(password)<8:
            print(
                '''make sure to have username longer than 3 symbols
            and password longer then 8 symbols''')
            return False
        else:    
            register_dict['properties']=dict()
            for key, item in properties.items():
                if item == '' or item==' ':
                    register_dict['properties'][key]=None
                else: 
                    register_dict['properties'][key]=item
            
            df = pd.json_normalize(register_dict) #create flattened dataframe (df)
            if os.stat(self.REGISTER_LOG_FILE).st_size==0: 
                #if file is empty write current df to json
                with open(self.REGISTER_LOG_FILE, "a") as file:
                    result = df.to_json(orient='records')
                    parsed = json.loads(result)
                    json.dump(parsed, file, sort_keys=False, indent=4)
            else:
                # else load existing data as df append current Serie and rewrite file
                self.save_to_json(self.REGISTER_LOG_FILE, df, overwrite=True)
            print('User has been registered.')
            return True

    
    def authenticate(self, username: str, password: str, path=None, in_method=False) -> bool:
        '''basic authentication '''
        if path==None: path=self.REGISTER_LOG_FILE
        
        if not os.path.isfile(path) or os.stat(path).st_size==0: 
            if in_method==False:
                print('Data file is empty')
            return False
        else:
            df=pd.read_json(path)
            df['username'] = df['username'].str.lower() # User names are case insensitive
            df["password"] = df["password"].astype(str) 
            return ((df.username==username) & (df.password==password)).any() #df.username.lower()
                
    

        
    
if __name__=='__main__':
    t=IdentityService('tt.json')
    t.register('mm5fm', '12345689f', **{'age':15, "sex": 'male'})
    t.register('mmcc5fm', '123453689f', **{'age':154, "sex": 'male'})