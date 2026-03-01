from enum import Enum

class ConstantHeader(Enum):
    HEADER_X_WHO = "x_who"    
    HEADER_X_NAME = "x_name"   
    HEADER_X_ID = "x_id"       
    HEADER_X_ROLE = "x_role"   
    HEADER_AUTH = "Authorization" 
    HEADER_X_PRIVILEGE = "x_privilege" 
    HEADER_X_CONTENT_TYPE = "Content-Type" 