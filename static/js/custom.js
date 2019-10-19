let mood = 10,
  energy = 5,
  preference = 2;

function showLoading() {
  const temp = document.getElementsByTagName("template")[0];
  const clon = temp.content.cloneNode(true);
  const content = document.getElementById("content");
  content.appendChild(clon);
}

async function clearContent() {
  const content = document.getElementById("content");
  while (content.firstChild) {
    content.removeChild(content.firstChild);
  }
}

function createTable() {
  var tbl = document.createElement("table");
  tbl.style.width = "100%";
  tbl.setAttribute("border", "1");
  var tbdy = document.createElement("tbody");
  for (var i = 0; i < 3; i++) {
    var tr = document.createElement("tr");
    for (var j = 0; j < 2; j++) {
      if (i == 2 && j == 1) {
        break;
      } else {
        var td = document.createElement("td");
        td.appendChild(document.createTextNode("\u0020"));
        i == 1 && j == 1 ? td.setAttribute("rowSpan", "2") : null;
        tr.appendChild(td);
      }
    }
    tbdy.appendChild(tr);
  }
  tbl.appendChild(tbdy);

  const content = document.getElementById("content");
  content.appendChild(tbl);
}

function showTable(results) {
  const content = document.getElementById("content");
  const table = document.createElement("table");
  table.id = "results";

  const header = document.createElement("tr");
  const hr0 = document.createElement("th");
  hr0.appendChild(document.createTextNode("#"));
  header.appendChild(hr0);
  const hr1 = document.createElement("th");
  hr1.appendChild(document.createTextNode("Artist"));
  header.appendChild(hr1);
  const hr2 = document.createElement("th");
  hr2.appendChild(document.createTextNode("Song"));
  header.appendChild(hr2);
  const hr3 = document.createElement("th");
  hr3.appendChild(document.createTextNode("Score"));
  header.appendChild(hr3);
  table.appendChild(header);

  for (let i = 0; i < 15; i++) {
    const row = document.createElement("tr");
    const td0 = document.createElement("td");
    td0.appendChild(document.createTextNode(`${i + 1}`));
    row.appendChild(td0);
    const td1 = document.createElement("td");
    td1.appendChild(document.createTextNode(results[i]["artist_name"]));
    row.appendChild(td1);
    const td2 = document.createElement("td");
    td2.appendChild(document.createTextNode(results[i]["track_name"]));
    row.appendChild(td2);
    const td3 = document.createElement("td");
    td3.appendChild(document.createTextNode(results[i]["musicScore"]));
    row.appendChild(td3);
    table.appendChild(row);
  }
  console.log(table, header);

  content.appendChild(table);
}

function submitResults() {
  clearContent();
  showLoading();
  axios
    .post("http://localhost:5000/find", {
      data: [mood, energy, preference]
    })
    .then(async function(response) {
      await clearContent();
      showTable(response.data);
    })
    .catch(function(error) {
      console.log(error);
    });
}
