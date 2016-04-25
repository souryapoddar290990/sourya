<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %> 
<%@ page import='java.util.*'%>
<!DOCTYPE html>
<html>
<head>
<title>Serial</title>
<link rel="stylesheet" href="style.css" type="text/css" >
<link href="jquery.mCustomScrollbar.css" rel="stylesheet" />
<script src="jquery.min.js"></script>
<script src="jquery.mCustomScrollbar.concat.min.js"></script>
<script>
(function($){
$(window).load(function(){
$("#serial2").mCustomScrollbar({
autoHideScrollbar:true,
theme:"light-blue"
});
});
})(jQuery);
</script>
</head>
<%
try {
String connectionURL = "jdbc:mysql://localhost/";
Connection connection = null;
Statement statement = null;
ResultSet rs = null;
String e,episode="",season="",dy="",mon="",yr="",monthn[] = {
            "", "January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"
        };  
Class.forName("com.mysql.jdbc.Driver").newInstance();
Connection conn=(Connection)getServletContext().getAttribute("connection");
String e1 = request.getParameter("Serial");
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
int day,month,year;
Calendar calendar = Calendar.getInstance();
year=calendar.get(Calendar.YEAR);
month=calendar.get(Calendar.MONTH)+1;
day=calendar.get(Calendar.DATE);
String query2="select count(*) from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&serial='"+e1+"'";
PreparedStatement ps2 = conn.prepareStatement(query2);
ResultSet rs2 = ps2.executeQuery();
while (rs2.next())
{episode=rs2.getString(1);}
query2 = "select season from t1 where serial='"+e1+"' order by season desc limit 0,1";
ps2 = conn.prepareStatement(query2);
rs2 = ps2.executeQuery();
while (rs2.next())
{season=rs2.getString(1);}
query2="select day,month,year from t1 where serial='"+e1+"' limit 0,1";
ps2 = conn.prepareStatement(query2);
rs2 = ps2.executeQuery();
while (rs2.next())
{
if(rs2.getInt(1)<10)
dy="0"+rs2.getString(1);
else
dy=rs2.getString(1);
mon=monthn[rs2.getInt(2)];
yr=rs2.getString(3);      
}
query2 = "select * from t2 where serial='"+e1+"'";
ps2 = conn.prepareStatement(query2);
rs2 = ps2.executeQuery();
while (rs2.next()) {
%>
<body background="images/<%=rs2.getString(1)%>/1.jpg" style="background-size:1366px 768px;background-attachment:fixed;background-repeat:no-repeat;">
<table id="stab">
<tr><td><a href="shows.jsp"><img src="images/wback.png" width="44" height="44" onMouseOver=src="images/wwback.png" onMouseOut=src="images/wback.png" onMouseDown=src="images/bbback.png"></a></td><td id="td0"><%out.print(e);%></td></tr>
</table>
<div style="width:374px;height:550px;margin-top:40px;margin-left:65px;border:1px white solid;">
<img src="images/<%=rs2.getString(1)%>/2.jpg">  
</div>
<div id="serial1">
<table id="tab10">
<tr><td id="td25">Information</td><td></td></tr>
<tr><td></td></tr>
<tr><td id="td24">Status:</td><td id="td26"><%=rs2.getString(3)%></td></tr>
<tr><td id="td24">Genre:</td><td id="td26"><%=rs2.getString(4)%></td></tr>
<tr><td id="td24">Network:</td><td id="td26"><%=rs2.getString(5)%></td></tr>
<tr><td id="td24">Runtime:</td><td id="td26"><%=rs2.getString(2)%> mins</td></tr>
<tr><td id="td24">Seasons:</td><td id="td26"><%out.print(season);%></td></tr>
<tr><td id="td24">Episodes:</td><td id="td26"><%out.print(episode);%></td></tr>
<tr><td id="td24">Started:</td><td id="td26"><%out.print(dy);%> <%out.print(mon);%> <%out.print(yr);%></td></tr>
</table>
<table id="tab10">
<tr><td></td><td></td></tr>
<tr><td id="td23">Theme</td><td></td></tr>
<tr><td id="td22"><%=rs2.getString(6)%></td></tr>
</table>  
<% } %>
</div>
<%
String query1 = "select season,serial from t1 where serial='"+e1+"' group by season order by season";
PreparedStatement ps1 = conn.prepareStatement(query1);
ResultSet rs1 = ps1.executeQuery();
%>
<div id="serial2">
<table id="tab11">
<%
while (rs1.next()) {
String a;
if(rs1.getInt(1)<10)
{a="0";}
else
{a="";}
%>
<tr><td id="td20"><a href='season.jsp?Serial=<%=rs1.getString(2)%>&Season=<%=rs1.getString(1)%>'>Season <span><%out.print(a);%><%=rs1.getString(1)%></span></a></td></tr>
<tr><td id="td21"></td></tr>
<% } %>
</table>
</div>
<%
rs1.close();
rs2.close();
statement.close();
} catch (Exception ex) {
}%>
</body>
</html>