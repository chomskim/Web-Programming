function csv2json(csv) {
  const lines = csv.split('\n');
  const result = [];
  const headers = lines[0].split(',');

  for (let i = 1; i < lines.length; i++) {
    const obj = {};
    const currentline = lines[i].split(',');

    for (let j = 0; j < headers.length; j++) {
      obj[headers[j]] = currentline[j];
    }

    result.push(obj);
  }

  return result; //JavaScript object
  //return r; //JSON
}
function filterName(list, name, valist) {
  const result = [];

  for (let i = 0; i < list.length; i++) {
    const obj = list[i];
    if (valist.indexOf(obj[name]) >= 0) {
      result.push(obj);
    }
  }
  return result;
}
function groupByDate(list) {
  const rows = [];
  const mapObj = {};
  for (let i = 0; i < list.length; i++) {
    const obj = list[i];
    const da = obj['date'];
    if (mapObj[da] == null) {
      mapObj[da] = [];
    }
    const nameNpr = (({ name, price }) => ({ name, price }))(obj);
    mapObj[da].push(nameNpr);
  }

  const dates = Object.keys(mapObj);
  for (let i = 0; i < dates.length; i++) {
    const da = dates[i];
    const row = { date: da, cols: mapObj[da] };
    rows.push(row);
  }
  return rows;
}
