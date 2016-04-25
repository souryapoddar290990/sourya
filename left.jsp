<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %> 
<%@ page import='java.util.*'%>
<!DOCTYPE html>
<html>
<head>
<title>Left</title>
<link rel="stylesheet" href="style.css" type="text/css" >
<link href="jquery.mCustomScrollbar.css" rel="stylesheet" />
<script src="jquery.min.js"></script>
<script src="jquery.mCustomScrollbar.concat.min.js"></script>
<script>
(function($){
$(window).load(function(){
$("#contentleft").mCustomScrollbar({
autoHideScrollbar:true,
theme:"light-blue"
});
});
})(jQuery);
</script>
</head>
<body id="shows">
<%
try {
String connectionURL = "jdbc:mysql://localhost/";
Connection connection = null;
Statement statement = null;
Class.forName("com.mysql.jdbc.Driver").newInstance();
Connection conn=(Connection)getServletContext().getAttribute("connection");
int day,month,year;
Calendar calendar = Calendar.getInstance();
year=calendar.get(Calendar.YEAR);
month=calendar.get(Calendar.MONTH)+1;
day=calendar.get(Calendar.DATE);
String query1 = "select serial,count(*) from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&seena='No' group by serial";
PreparedStatement ps1 = conn.prepareStatement(query1);
ResultSet rs1 = ps1.executeQuery();
%>
<table id="stab">
<tr><td><a href="shows.jsp"><img src="images/bback.png" width="44" height="44" onMouseOver=src="images/wbbback.png" onMouseOut=src="images/bback.png" onMouseDown=src="images/bbback.png"></a></td><td id="tv">Unwatched</td><td id="shows">Episodes</td></tr>
</table>
<div id="serltab1">
<table id="tabser">
<tr><td>Arya</td></tr>  
<tr><td id="blank"></td></tr>
</table>
<div id="leftarya">
<%
while(rs1.next()) {
%>
<a href="left.jsp?Serial=<%=rs1.getString(1)%>&User=seena&sday=<%out.print(day);%>&smonth=<%out.print(month);%>&syear=<%out.print(year);%>">
<table id="left">
<tr id="left">
<td id="td27"><img src="images/<%=rs1.getString(1)%>/3.jpg" height="56" width="304"></td>
<td id="td28"><%=rs1.getString(2)%></td>
</tr>
</table>
</a>
<% } %>
</div>
</div>
<%
String query2 = "select serial,count(*) from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&seen='No' group by serial";
PreparedStatement ps2 = conn.prepareStatement(query2);
ResultSet rs2 = ps2.executeQuery();
%>
<div id="serltab2">
<table id="tabser">
<tr><td>Sourya</td></tr>  
<tr><td id="blank"></td></tr>
</table>
<div id="leftsourya">
<%
while(rs2.next()) {
%>
<a href="left.jsp?Serial=<%=rs2.getString(1)%>&User=seen&sday=<%out.print(day);%>&smonth=<%out.print(month);%>&syear=<%out.print(year);%>">
<table id="left">
<tr id="left">
<td id="td29"><%=rs2.getString(2)%></td>
<td id="td27"><img src="images/<%=rs2.getString(1)%>/3.jpg" height="56" width="304"></td>
</tr>
</table>
</a>
<% } %>
</div>
</div>
<form action="left" method="POST" name="myform" id="myform">
<div id="contentleft">
 <%
String e1 = request.getParameter("Serial");
String e2 = request.getParameter("User");
String query = "select name,season,episode from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&serial='"+e1+"'&&"+e2+"='No'";
PreparedStatement ps = conn.prepareStatement(query);
ResultSet rs = ps.executeQuery();
%>
<table style="border-collapse:collapse;">
<%
while (rs.next()) 
{
String a;    
if(rs.getInt(3)<10)
{a="0";}
else
{a="";}    
    %>
    <tr>
        <td style="padding:0px 10px 0px 20px;"><a href='season.jsp?Serial=<%out.print(e1);%>&Season=<%=rs.getString(2)%>&Episode=<%=rs.getString(3)%>' style="text-decoration:none;color:#008dd5;"><%=rs.getString(1)%></a></td>
        <td style="color:#d6ac30;"><%=rs.getString(2)%><span style="color:#008ddf;">-</span><span style="color:black;"><%out.print(a);%><%=rs.getString(3)%></span></td>
        <td style="padding-left:15px;"><button id="yn" type="submit" value="<%out.print(e1);%>,<%=rs.getString(2)%>,<%=rs.getString(3)%>,<%out.print(e2);%>,<%out.print(day);%>,<%out.print(month);%>,<%out.print(year);%>" name="temp" /><img src="images/yes.png"></td>
    </tr>
    <%}%>
</table>        
</div>
</form>
<%
rs.close();
rs1.close();
rs2.close();
statement.close();
} catch (Exception ex) {
}%>
</body>
</html>