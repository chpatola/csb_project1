# csb_project1
This repository contains project 1 for this course: https://cybersecuritybase.mooc.fi/
In this repository, 5 of OWASP Top 10 Web Application Security Risks are described with examples(https://owasp.org/www-project-top-ten/)


## installation instructions: 
Dependencies (or how to copy the env in conda) : csb_project1/content/fsecure_project1.yaml
User to test with: mia & password miamia0000


## FLAW 1: SQL injection
### Description of flaw 1:
Flaw 1 is SQL injection. This means that it  is possible to use other sql queries than what has been intended. If the attended query was one to select the names of the capital cities located in Europe, a hacker could modify the query to,for example, access content from other tables (person data?), empty the whole table or insert own data into it.

In my code, the SQL injection flaw can be found in content/views.py on lines 33-38. Here, a connection has been made via python’s connect() function and then the cursor() function has been used to execute a basic sql insert query via executescript(). This function executes all sql queries that  is given to it. Hence, there is nothing stopping a hacker from doing all kinds of modification to the query. He/she could, for example empty the whole table by writing '); DELETE FROM CITIES; -- in the form’s text area. If one would have used execute(), several queries would not have been possible to execute, but a hacker could still, for example, access data from other tables via UNION.

```
    #Incorrect database insert
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    strinifyed_pub_date = str(city_pub)
    sql = "INSERT INTO CITIES (city_name, pub_date, description) VALUES ('"+ city_name+"','"+strinifyed_pub_date+"','"+city_description+"')"
    result = cursor.executescript(sql)
    conn.commit()
    return HttpResponseRedirect('/')
```    

### How to fix it:
The best way to fix sql injection vulnerabilities is to make use of the framework’s provided database functionality. In Django, it means to make use of the model classes, which makes it possible to sanitize input. For example, if one thinks about selection of capital cities located in Europe, the selection part (located in….) would be “capsulated” into a model field. Data from the correct part of the selection form would only be evaluated within that specific column.

In my code, this suggested fix is on lines 28-30 of content/views.py.

```
#Correct database insert
#city = Cities(city_name=city_name,description= city_description, pub_date = city_pub)
#city.save()`
```
## FLAW 2: Using Components with Known Vulnerabilities. (plus Insecure Deserialization)

### Description of flaw 2:
A common flaw in software applications is that they use components with known vulnerabilities. It is understandable, that libraries, components, and other tools developed by humans aren’t flawless and exposed vulnerabilities are corrected in newer versions. Therefore, it is important to always use up to date versions of components and be aware of possible newly found vulnerabilities that have not yet been fixed.

In my code, I use the function numpy.load() from numpy 1.11.3 (content/fsecure_project1.ya63. This function has been found to have a vulnerability in Jan 2019: https://cyware.com/news/critical-vulnerability-in-numpy-could-allow-attackers-to-perform-remote-code-execution-33117832
 
### How to fix it:
If I would have updated numpy to the current version, I would have needed to manually set the argument allow_pickle=TRUE in order to be exposed to the vulnerability. If I understand how to safely deserialize, I can then consciously take the choice to use the function with pickle. Otherwise, I would have to choose another way to make use of my model (content/ml_model.py) 

…
## FLAW 3: Sensitive Data Exposure

### Description of flaw 3:
There are several ways how sensitive data could get into the wrong hands. One way is that the sensitive data has not been recognized properly and thus not encrypted in the database. This is the case in my application content/models.py. The user data model where social security number has not been encrypted is on lines 17-25. The model is receiving user input in content/views.py on lines 45-55.

``` 
#Non existing handling of sensitive data (models.py)
class UserData(models.Model):
    name = models.CharField(max_length=100)
    social_security = models.CharField(max_length=11)
    my_issue = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'USERDATA'
```
```
#Database input using table with no encryption of social security data  (views.py)
    userdata = UserData(name=name_in,social_security = social_security_in,my_issue=my_issue_in)
    userdata.save()      
```
### How to fix it:
The first step would be to recognise sensitive data and encrypt it. There are different ways to do this. A simple way to encrypt is shown in content/models.py on line 8-14.
In addition to this, network protection should be taken into consideration and https protocol favoured over http.

```
#Correct sensitive data handling
class OurUsers(models.Model):
    name = models.CharField(max_length=100)
    social_security =EncryptedTextField(max_length=11)
    my_issue = models.TextField()

    class Meta:
        db_table = 'OURUSERS'   
```
## FLAW 4:Insufficient Logging & Monitoring

### Description of flaw 4:
Not logging and monitoring events taking place via the application, especially information related to logins and user activity, poses a significant security risk, as unwanted user/hacker behaviour won’t be noticed or will be noticed with delay.

In my application, I have one view which requires login, machinelearning (content/views.py). In the current state of the application, there are no logs of logins and attempted logins (content/model.py).

### How to fix it:
Functionality for logging login activities can be found in content/models.py on line 38 and forward. The functionality can be taken into use in the admin portal by commenting back the content in contetn/admin.py lines 6 and 13-16. With this functionality, one can see logins and login attempts in the admin portal. Additional functionality that could be added is, among others, threshold for login attempts and alerts for different suspicious login attempts.

```
# Class AuditEntry in content/models.py
class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    AuditEntry.objects.create(action='user_login_failed', username=credentials.get('username', None))
```
```
# Admin AuditEntry into use in admin meny via admin.py
@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip',]
    list_filter = ['action',]
```    

## FLAW 5:Broken Access Control.
### Description of flaw 5: 
Access control is about making sure that users can only do what is intended and not get access to content they shouldn’t. 

In my code, the view machinelearning
 (content/views.py) on line 61 and forward is attended only to be seen by admin users. I do check that the user is logged in before allowing access, but I do not check if she/he has gotten admin rights.

### How to fix it:
In order to make the view accessible only by admin users, I need to explicitly check that their credentials are indeed admin level. This can be done with the codes on lines 57-60 in content/views.py.

```
def check_admin(user):
   return user.is_superuser

@user_passes_test(check_admin,login_url='/fail')   
@login_required
def machinelearning(request):
    loaded_model = np.load('finalized_model.P')
    #Here we will use the model and then we will output the result to ml.html
    return render(request, 'content/ml.html')
```    
