function csv2json(csv){

  var lines=csv.split("\n");

  var result = [];

  var headers=lines[0].split(",");

  for(var i=1;i<lines.length;i++){

	  var obj = {};
	  var currentline=lines[i].split(",");

	  for(var j=0;j<headers.length;j++){
		  obj[headers[j]] = currentline[j];
	  }

	  result.push(obj);

  }
  
  return result; //JavaScript object
  //return r; //JSON
}
function filterName(list, name, valist) {
    var result = [];
    
    for(var i=0;i<list.length;i++) {
        var obj = list[i];
        if (valist.indexOf(obj[name]) >= 0) {
            result.push(obj);
        }
    }
    return result;
}
function groupByDate(list) {
    var rows = []
    var map = {}
    for(var i=0;i<list.length;i++) {
        var obj = list[i];
        var da = obj['date'];
        if (map[da]==null) {
            map[da] = [];
        }
        const nameNpr = (({ name, price }) => ({ name, price }))(obj);
        map[da].push(nameNpr);
    }
    
    dates = Object.keys(map);
    for(var i=0;i<dates.length;i++) {
        var da = dates[i];
        const row = {date:da, cols:map[da]}
        rows.push(row)
    }    
    return rows
}