from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
import bcrypt, re
from django.db import connection
import sqlite3

# Create your views here.
def isValidEmail(email):
	if len(email) < 7 or re.match(r'[^@]+@[^@]+\.[^@]+', email) == None:
		return "Email should be of valid format. Format example@example.xxx."
	return True	

def isValidName(name):
	if len(name) < 2:
		return "must be 2 or more characters long"	
	return True
	
def isValidPwdLen(pwd):
	if len(pwd) < 8:
		return "Password must be of minimum 8 characters long"
	return True
	return False	
		
def isPwdMatchesConfirmPwd(pwd, cPwd):
	if pwd != cPwd:
		return "Passwords do not match"
	return True	

def index(request):
	if 'logged_in_user' not in request.session:
		request.session['logged_in_user'] = ""

	if 'email' not in request.session:
		request.session['email'] = ""

	if 'user_id' not in request.session:
		request.session['user_id'] = ""

	return render(request, "main/index.html", {})

def login(request):			
	err_msg = ""
	form_email = request.POST['email']	
	form_pwd = request.POST['password']	
	
	if (form_email == ""):
		err_msg += "Email cannot be empty\n\n"	
	elif isValidEmail(form_email) != True:
		err_msg += isValidEmail(form_email) + " \n\n"
		
	if (form_pwd == ""):
		err_msg += "Password cannot be empty\n\n"	
		
	if len(err_msg) > 0:		
		messages.error(request, err_msg, "")
		return redirect("/")
	
	err_msg = User.objects.login_validator(request.POST)
	
	if len(err_msg) > 0:	
		for tag, error in err_msg.iteritems():
			messages.error(request, error, "")
		return redirect("/")
	
	form_email = form_email.lower().strip()
	users = User.objects.filter(email = form_email)	
	
	request.session['logged_in_user'] = users[0].name
	request.session['email'] = form_email
	request.session['user_id'] = users[0].id
		
	return redirect("/poke_dashboard")
	
def register_user(request):	
	err_msg = ""
	form_name = request.POST['name']
	form_alias = request.POST['alias']
	form_email = request.POST['email']	
	form_pwd = request.POST['password']
	form_confirm_pwd = request.POST['confirm_password']
	form_dob = request.POST['dob']
	
	if(form_name == ""):		
		err_msg += "Name cannot be empty\n\n"	
	elif isValidName(form_name) != True:
		err_msg += "Name " + isValidName(form_name) + "\n\n"
				
	if(form_alias == ""):		
		err_msg += "Alias cannot be empty\n\n"		
	elif isValidName(form_alias) != True:
		err_msg += "Alias " + isValidName(form_alias) + "\n\n"
		
	if (form_email == ""):
		err_msg += "Email cannot be empty\n\n"	
	elif isValidEmail(form_email) != True:
		err_msg += isValidEmail(form_email) + " \n\n"
		
	if (form_confirm_pwd == ""):
		err_msg += "Confirm password cannot be empty and must be same as the password\n\n"
		
	if (form_pwd == ""):
		err_msg += "Password cannot be empty\n\n"		
	elif isValidPwdLen(form_pwd) != True:
		err_msg += isValidPwdLen(form_pwd) + "\n\n"	
	elif isPwdMatchesConfirmPwd(form_pwd, form_confirm_pwd) != True:
		err_msg += isPwdMatchesConfirmPwd(form_pwd, form_confirm_pwd) + "\n\n"
	
	if form_dob == "":
		err_msg += "Date of Birth cannot be empty\n"
	else:
		form_dob = datetime.strptime(form_dob, '%Y-%m-%d')
		
	if len(err_msg) > 0:		
		messages.error(request, err_msg, "")
		return redirect("/")		
	
	form_email = form_email.lower().strip()
	hash_pwd = bcrypt.hashpw(form_pwd.encode(), bcrypt.gensalt())
	
	User.objects.create(name=form_name, alias=form_alias, email=form_email, password=hash_pwd, dob=form_dob, created_at=datetime.now() )
	users = User.objects.filter(email = form_email)	
	request.session['logged_in_user'] = form_name.title()
	request.session['email'] = form_email	
	request.session['user_id'] = users[0].id
		
	return redirect("/poke_dashboard")
		
def logout(request):
	request.session['logged_in_user'] = ""		
	return redirect("/")

def poke_dashboard(request):		
	cursor = connection.cursor()	
	cursor.execute("select count(*) from (select * from main_poke where main_poke.user_who_is_poked_id={poker} group by main_poke.poker_id) as count".format(poker=request.session['user_id']))	
	no_of_tmes_u_r_poked = cursor.fetchall()
	
	cursor = connection.cursor()
	cursor.execute("select main_user.name, count(*) from main_poke join main_user on main_user.id = main_poke.poker_id where main_poke.user_who_is_poked_id={poker} group by main_poke.poker_id order by count(*) desc".format(poker=request.session['user_id']))		
	users_who_poked_u = cursor.fetchall()
	
	cursor = connection.cursor()
	#cursor.execute("select main_user.name, main_user.alias, main_user.email, count(*), main_user.id from main_user left join main_poke on main_poke.user_who_is_poked_id = main_user.id where main_user.id not in ({poker}) group by main_user.id".format(poker=request.session['user_id']))	
	cursor.execute("select main_user.name, main_user.alias, main_user.email, count(*), main_user.id from main_user join main_poke on main_poke.user_who_is_poked_id = main_user.id where main_user.id not in ({poker}) group by main_user.id".format(poker=request.session['user_id']))	
	other_users = cursor.fetchall()
	
	cursor = connection.cursor()	
	cursor.execute("select main_user.name, main_user.alias, main_user.email, main_user.id from main_user where main_user.id not in ({poker}) and main_user.id not in (select main_user.id from main_user join main_poke on main_poke.user_who_is_poked_id = main_user.id where main_user.id not in ({poker}) group by main_user.id)".format(poker=request.session['user_id']))	
	other_users1 = cursor.fetchall()
	
	
	context = {
		'other_users': other_users,
		'no_of_tmes_u_r_poked': no_of_tmes_u_r_poked,
		'users_who_poked_u': users_who_poked_u,
		'other_users1': other_users1,
	}
	
	return render(request, "main/poke_dashboard.html", context)
	
def pokes(request, id):	
	cursor = connection.cursor()
	cursor.execute("INSERT INTO main_poke (poker_id, user_who_is_poked_id) VALUES ({poker}, {getting_poked})".\
        format(poker=request.session['user_id'], getting_poked=id))
	poke_data = cursor.fetchall()	
	
	return redirect("/poke_dashboard")
	
	
