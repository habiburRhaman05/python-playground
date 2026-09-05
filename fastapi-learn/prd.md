app name = instant blog 

agenda - this a fastapi based backend api for covering blogs apis features 

roles - Admin / User

functional requrements : 

normal user features: 
. user authentication (register,login,update profile, get profile info,forgot password, email verify - optional)
. user can upload blog post with title,description,photo,tags etc
. user can like and comment(one level)
. user can delete own post / also post can be editable
. user can chnage status of post like achive or puslish 

admin feature : 

admin can view all users ,
admin can  update status of user - banned or unbanned

non-functional requrements : 

use basic security,
use role based authorization + dependency injection


