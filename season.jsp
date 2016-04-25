<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %> 
<%@ page import='java.util.*'%>
<html>
<head>
<title>Season</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="style.css" type="text/css" >
<link href="jquery.mCustomScrollbar.css" rel="stylesheet" />
<script src="jquery.min.js"></script>
<script src="jquery.mCustomScrollbar.concat.min.js"></script>
<script>
(function($){
$(window).load(function(){
$("#ssn").mCustomScrollbar({
autoHideScrollbar:true,
theme:"light-white"
});
});
})(jQuery);
</script>
</head>
<%
try {
String a,b,c,d,dy,mon,yr,monthn[] = {
            "", "January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"
        };    
String connectionURL = "jdbc:mysql://localhost/";
Connection connection = null;
Statement statement = null;
Class.forName("com.mysql.jdbc.Driver").newInstance();
Connection conn=(Connection)getServletContext().getAttribute("connection");
String e1 = request.getParameter("Serial");
String e2 = request.getParameter("Season");
String e3 = request.getParameter("Episode");
%>
<body background="images/<%out.print(e1);%>/1.jpg" style="background-size:1366px 768px;background-attachment:fixed;background-repeat:no-repeat;">
<%
String e;
if(e1.equals("How Its Made"))
{e="How It's Made";}
else
{
if(e1.equals("Tom Jerry"))
{e="Tom & Jerry";}
else
{
if(e1.equals("Marvels Agents Of Shield"))
{e="Marvel's Agents Of Shield";}
else
{       
e=e1;
}
}   
}
String query1 = "select name,episode,day,month,year from t1 where Serial='"+e1+"'&&Season='"+e2+"' ";
PreparedStatement ps1 = conn.prepareStatement(query1);
ResultSet rs1 = ps1.executeQuery();
%>
<table id="stab">
<tr><td><a href='serial.jsp?Serial=<%out.print(e1);%>'><img src="images/wback.png" width="44" height="44" onMouseOver=src="images/wwback.png" onMouseOut=src="images/wback.png" onMouseDown=src="images/bbback.png"></a></td><td id="td0"><%out.print(e);%></td><td id="td">Season <%out.print(e2);%></td></tr>
</table>
<div id="ssn">
    <%
while (rs1.next()) {
if(rs1.getInt(3)==0)
{
dy="";
mon="";
yr="";
}
else
{    
if(rs1.getInt(3)<10)
{dy="0"+rs1.getString(3);}
else
{dy=""+rs1.getString(3);}
mon=monthn[rs1.getInt(4)];
yr=rs1.getString(5);
}
if(rs1.getInt(2)<10)
{a="0";}
else
{a="";}
%>
<a href="season.jsp?Serial=<%out.print(e1);%>&Season=<%out.print(e2);%>&Episode=<%=rs1.getString(2)%>">
<table background="images/<%out.print(e1);%>/<%out.print(e2);%>/<%out.print(a);%><%=rs1.getString(2)%>.png" style="border-collapse:collapse; background-size:312px 176px;">
<tr><td id="td6"></td></tr>
<tr><td id="td7"><%out.print(a);%><%=rs1.getString(2)%> - <%=rs1.getString(1)%></td></tr>
<tr><td id="td8"><%out.print(dy);%> <%out.print(mon);%> <%out.print(yr);%></td></tr>
</table></a>
<table><tr><td id="td9"></td></tr></table>
<%}%>
</div>
<form action="change" method="POST" name="myform" id="myform">
<%
String query = "select name,seena,seen,sub,day,month,year,summary from t1  where Serial='"+e1+"'&&Season='"+e2+"'&&Episode='"+e3+"'";
PreparedStatement ps = conn.prepareStatement(query);
ResultSet rs = ps.executeQuery();
while (rs.next()) {
if(rs.getInt(5)==0)
{
dy="";
mon="";
yr="";
}
else
{    
if(rs.getInt(5)<10)
{dy="0"+rs.getString(5);}
else
{dy=""+rs.getString(5);}
mon=monthn[rs.getInt(6)];
yr=rs.getString(7);
}
if(rs.getString(2).equals("No"))
{b="yes";}
else
{b="no";}   
if(rs.getString(3).equals("No"))
{c="yes";}
else
{c="no";} 
if(rs.getString(4).equals("No"))
{d="yes";}
else
{
if(rs.getString(4).equals("Yes"))
{d="no";}
else
{d="na";}
}
if(e3.equals("1")||e3.equals("2")||e3.equals("3")||e3.equals("4")||e3.equals("5")||e3.equals("6")||e3.equals("7")||e3.equals("8")||e3.equals("9"))
{a="0";}
else
{a="";}     
%>
<div id="content">
<table id="etab">
<tr><td colspan="3" id="td1"><%=rs.getString(1)%></td></tr>
<tr><td rowspan="6" id="td10"><a href="video/<%out.print(e1);%>/<%out.print(e2);%>/<%out.print(a);%><%out.print(e3);%> - <%=rs.getString(1)%> - Shortcut.lnk"><img src="images/<%out.print(e1);%>/<%out.print(e2);%>/<%out.print(a);%><%out.print(e3);%>.png"><span id="download">Click to download</span></a></td>
<td id="td2">Aired On:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td id="td3" colspan="2"><%out.print(dy);%> <%out.print(mon);%> <%out.print(yr);%></td></tr>
<tr><td id="td2">Season:</td><td id="td3"><%out.print(e2);%></td></tr>
<tr><td id="td2">Episode:</td><td id="td3"><%out.print(e3);%></td></tr>
<tr><td id="td2">Arya:</td><td id="td3"><%=rs.getString(2)%></td><td><button id="yn" type="submit" value="seena,<%out.print(b);%>,<%out.print(e1);%>,<%out.print(e2);%>,<%out.print(e3);%>" name="temp" /><img src="images/<%out.print(b);%>.png"></td></tr>
<tr><td id="td2">Sourya:</td><td id="td3"><%=rs.getString(3)%></td><td><button id="yn" type="submit" value="seen,<%out.print(c);%>,<%out.print(e1);%>,<%out.print(e2);%>,<%out.print(e3);%>" name="temp" /><img src="images/<%out.print(c);%>.png"></td></tr>
<tr><td id="td2">Subtitle:</td><td id="td3"><%=rs.getString(4)%></td><td><button id="yn" type="submit" value="sub,<%out.print(d);%>,<%out.print(e1);%>,<%out.print(e2);%>,<%out.print(e3);%>" name="temp" /><img src="images/<%out.print(d);%>.png"></td></tr>
</table>
<table>
<tr><td id="td4">Summary</td></tr>
<tr><td id="td5"><%=rs.getString(8)%></td></tr>
</table>    
<% }
rs.close();
rs1.close();
statement.close();
} catch (Exception ex) {
}%>    
</div>
</form>
</body>
</html>
