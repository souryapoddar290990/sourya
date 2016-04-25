<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %> 
<%@ page import='java.util.*'%>
<!DOCTYPE html>
<html>
<head>
<title>Shows</title>
<link rel="stylesheet" href="style.css" type="text/css" >
</head>
<body id="shows">
<%
try {
String connectionURL = "jdbc:mysql://localhost/";
Connection connection = null;
Statement statement = null;
Class.forName("com.mysql.jdbc.Driver").newInstance();
Connection conn=(Connection)getServletContext().getAttribute("connection");
String query1 = "select serial from t2 order by serial limit 0,6";
PreparedStatement ps1 = conn.prepareStatement(query1);
ResultSet rs1 = ps1.executeQuery();
%>
<table id="htab">
<tr><td id="tv">TV</td><td id="shows">Shows</td></tr>
</table>
<div id="stat">
<table id="stat">
<%
int day,month,year;
Calendar calendar = Calendar.getInstance();
year=calendar.get(Calendar.YEAR);
month=calendar.get(Calendar.MONTH)+1;
day=calendar.get(Calendar.DATE);
String query="select count(t1.name),t2.runtime*count(t1.name) from t1,t2 where (t1.day+t1.month*30+t1.year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&t1.seena='No'&&(t1.serial=t2.serial) group by t1.serial";
PreparedStatement ps = conn.prepareStatement(query);
ResultSet rs = ps.executeQuery();
int episodea=0,timea=0,episodes=0,times=0;
while (rs.next()) 
{
timea=timea+rs.getInt(2);
episodea=episodea+rs.getInt(1);
}
query="select count(t1.name),t2.runtime*count(t1.name) from t1,t2 where (t1.day+t1.month*30+t1.year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&t1.seen='No'&&(t1.serial=t2.serial) group by t1.serial";
ps = conn.prepareStatement(query);
rs = ps.executeQuery();
while (rs.next()) 
{
times=times+rs.getInt(2);
episodes=episodes+rs.getInt(1);
}
String a1,a2,s1,s2;
int ad,ah,am,sd,sh,sm;
ad=timea/1440;
ah=timea/60;
ah=ah%24;
am=timea%60;
sd=times/1440;
sh=times/60;
sh=sh%24;
sm=times%60;
if(ah<10)
{a1="0";}
else
{a1="";}
if(sh<10)
{s1="0";}
else
{s1="";}
if(am<10)
{a2="0";}
else
{a2="";}
if(sm<10)
{s2="0";}
else
{s2="";}
%>
<tr><td id="td16">viewers</td><td id="td15">episodes</td><td id="td15">days</td><td id="td15">hours</td><td id="td15">minutes</td></tr>
<tr><td id="td11">Arya</td><td id="td18"><%out.print(episodea);%></td><td id="td12"><%out.print(ad);%><td id="td12"><%out.print(a1);out.print(ah);%><td id="td12"><%out.print(a2);out.print(am);%></td></tr>
<tr><td id="td13">Sourya</td><td id="td14"><%out.print(episodes);%></td><td id="td14"><%out.print(sd);%><td id="td14"><%out.print(s1);out.print(sh);%><td id="td14"><%out.print(s2);%><%out.print(sm);%></td></tr>
</table>
</div>
<div id="extra1">
<a href="left.jsp" id="ue"><img src="images/uwe.png"></a>          
</div>
<div id="extra2">
<a href="soon.jsp" id="ue"><img src="images/uce.png"></a>         
</div>
<div id="sertab1">
<table id="tabser">
<%
while (rs1.next()) {
%>
<tr><td><a href='serial.jsp?Serial=<%=rs1.getString(1)%>'><img src="images/<%=rs1.getString(1)%>/3.jpg"></a></td></tr>
<tr><td id="hblnkr"></td></tr>
<% } %>
</table>
</div>
<%
String query2 = "select serial from t2 order by serial limit 6,6";
PreparedStatement ps2 = conn.prepareStatement(query2);
ResultSet rs2 = ps2.executeQuery();
%>
<div id="sertab2">
<table id="tabser">
<%
while (rs2.next()) {
%>
<tr><td><a href='serial.jsp?Serial=<%=rs2.getString(1)%>'><img src="images/<%=rs2.getString(1)%>/3.jpg"></a></td></tr>
<tr><td id="hblnkr"></td></tr>
<% } %>
</table>
</div>
<%
String query3 = "select serial from t2 order by serial limit 12,6";
PreparedStatement ps3 = conn.prepareStatement(query3);
ResultSet rs3 = ps3.executeQuery();
%>
<div id="sertab3">
<table id="tabser">
<%
while (rs3.next()) {
%>
<tr><td><a href='serial.jsp?Serial=<%=rs3.getString(1)%>'><img src="images/<%=rs3.getString(1)%>/3.jpg"></a></td></tr>
<tr><td id="hblnkr"></td></tr>
<% } %>
</table>
</div>
<%
String query4 = "select serial from t2 order by serial limit 18,6";
PreparedStatement ps4 = conn.prepareStatement(query4);
ResultSet rs4 = ps4.executeQuery();
%>
<div id="sertab4">
<table id="tabser">
<%
while (rs4.next()) {
%>
<tr><td><a href='serial.jsp?Serial=<%=rs4.getString(1)%>'><img src="images/<%=rs4.getString(1)%>/3.jpg"></a></td></tr>
<tr><td id="hblnkr"></td></tr>
<% } %>
</table>
</div>
<%
String query5 = "select serial from t2 order by serial limit 24,6";
PreparedStatement ps5 = conn.prepareStatement(query5);
ResultSet rs5 = ps5.executeQuery();
%>
<div id="sertab5">
<table id="tabser">
<%
while (rs5.next()) {
%>
<tr><td><a href='serial.jsp?Serial=<%=rs5.getString(1)%>'><img src="images/<%=rs5.getString(1)%>/3.jpg"></a></td></tr>
<tr><td id="hblnkr"></td></tr>
<% } %>
</table>
</div>
<%
String query6 = "select serial from t2 order by serial limit 30,6";
PreparedStatement ps6 = conn.prepareStatement(query6);
ResultSet rs6 = ps6.executeQuery();
%>
<div id="sertab6">
<table id="tabser">
<%
while (rs6.next()) {
%>
<tr><td><a href='serial.jsp?Serial=<%=rs6.getString(1)%>'><img src="images/<%=rs6.getString(1)%>/3.jpg"></a></td></tr>
<tr><td id="hblnkr"></td></tr>
<% } %>
</table>
</div>
<%
rs.close();
rs1.close();
rs2.close();
rs3.close();
rs4.close();
rs5.close();
rs6.close();
statement.close();
} catch (Exception ex) {
}%>
</body>
</html>