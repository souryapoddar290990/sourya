<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %> 
<%@ page import='java.util.*'%>
<!DOCTYPE html>
<html>
<head>
<title>Soon</title>
<link rel="stylesheet" href="style.css" type="text/css" >
</head>
<body id="shows">
<table id="stab">
<tr><td><a href="shows.jsp"><img src="images/bback.png" width="44" height="44" onMouseOver=src="images/wbbback.png" onMouseOut=src="images/bback.png" onMouseDown=src="images/bbback.png"></a></td><td id="tv">Upcoming</td><td id="shows">Episodes</td></tr>
</table>  
<br>
<%
String connectionURL = "jdbc:mysql://localhost/";
Connection connection = null;
Statement statement = null;
Class.forName("com.mysql.jdbc.Driver").newInstance();
Connection conn=(Connection)getServletContext().getAttribute("connection");
int day,month,year,monthnext,yearnext;
Calendar calendar = Calendar.getInstance();
year=calendar.get(Calendar.YEAR);
month=calendar.get(Calendar.MONTH)+1;
day=calendar.get(Calendar.DATE);
if(month==12)
{monthnext=1;yearnext=year+1;}
else
{monthnext=month+1;yearnext=year;}
String mon="",a="",dy="";   
String query1 = "select serial,name,season,episode,day,month,year from t1 where (day>"+day+"&&month="+month+"&&year="+year+")||(day<="+day+"&&month="+monthnext+"&&year="+yearnext+") order by year,month,day;";
PreparedStatement ps1 = conn.prepareStatement(query1);
ResultSet rs1 = ps1.executeQuery();
int i=0,leftcount;
String left="",top="";
    while (rs1.next()) { 
    if(i==0)    
    {top="margin-top:0px";left="margin-left:50px;";}
    if(i>1&&i%2==0)
    {
    top="margin-top:-532px;";
    leftcount=182*i/2+50; 
    left="margin-left:"+leftcount+"px;";
    }
    if(i>1&&i%2==1)
    {
    top="margin-top:0px;";
    leftcount=182*(i-1)/2+50;
    left="margin-left:"+leftcount+"px;";    
    }    
    if(rs1.getInt(5)<10)
    {dy="0"+rs1.getInt(5);}
    else
    {dy=""+rs1.getInt(5);}
    if(rs1.getInt(4)<10)
    {a="0";}
    else
    {a="";}
    if(rs1.getInt(6)<10)
    {mon="0"+rs1.getInt(6);}
    else
    {mon=""+rs1.getInt(6);}
    i++;
   %>
<div style="box-shadow:#212121 -7px 5px 7px;height:243px;width:151px;<%out.print(left);%><%out.print(top);%>">
<div id="soondate"><%out.print(dy);%>-<%out.print(mon);%>-<%=rs1.getString(7)%></div>
<div id="soonborder">&nbsp;</div>
<table background="images/<%=rs1.getString(1)%>/2.jpg" style="border-collapse:collapse;background-size:151px 222px;;text-align:center;color:white;font-family:Segoe UI;">
<tr><td id="soonpics">&nbsp;</td></tr>
<tr><td id="soondetails">Season <%=rs1.getString(3)%> Episode <%out.print(a);%><%=rs1.getString(4)%></td></tr>
<tr><td id="soonname"><%=rs1.getString(2)%></td></tr>
</table>
</div>
<br>
<%}rs1.close();%>
</body>
</html>