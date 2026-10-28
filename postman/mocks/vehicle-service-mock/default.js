const http = require('http');
const PORT = process.env.PORT || 4500;

const server = http.createServer((req, res) => {
  const { method, url } = req;

  // @endpoint GET /vehicles
  if (method === 'GET' && url === '/vehicles') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify([
      {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864
      },
      {
        "id": 2,
        "nickName": "Dolly",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 59000
      }
    ]));
    return;
  }

  // @endpoint POST /vehicles
  if (method === 'POST' && url === '/vehicles') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      let parsed = {};
      try { parsed = JSON.parse(body); } catch (e) {}
      if (!parsed.vin) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ "message": "Request body missing required attribute: vin" }));
        return;
      }
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        "id": 1,
        "nickName": parsed.nickName || "The Lisa Marie",
        "vin": parsed.vin || "4M2DV11W4RDJ53329",
        "make": parsed.make || "Mercury",
        "model": parsed.model || "Villager",
        "year": parsed.year || "1994",
        "miles": parsed.miles ? String(parsed.miles).replace(/\B(?=(\d{3})+(?!\d))/g, ',') : "159,864"
      }));
    });
    return;
  }

  // @endpoint GET /vehicles/:id
  const getVehicleMatch = url.match(/^\/vehicles\/(\d+)$/);
  if (method === 'GET' && getVehicleMatch) {
    const id = parseInt(getVehicleMatch[1]);
    if (id === 0 || id > 100) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ "message": `Vehicle with id: ${id} not found.` }));
      return;
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      "id": id,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159864
    }));
    return;
  }

  // @endpoint PUT /vehicles/:id
  const updateVehicleMatch = url.match(/^\/vehicles\/(\d+)$/);
  if ((method === 'PUT' || method === 'PATCH') && updateVehicleMatch) {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      let parsed = {};
      try { parsed = JSON.parse(body); } catch (e) {}
      const id = parseInt(updateVehicleMatch[1]);
      if (!parsed.nickName && !parsed.vin && !parsed.make && !parsed.model && !parsed.year && !parsed.miles) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ "message": "Bad request body." }));
        return;
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        "id": id,
        "nickName": parsed.nickName || "The Lisa Marie",
        "vin": parsed.vin || "4M2DV11W4RDJ53329",
        "make": parsed.make || "Mercury",
        "model": parsed.model || "Villager",
        "year": parsed.year || "1994",
        "miles": parsed.miles || 159999
      }));
    });
    return;
  }

  // @endpoint DELETE /vehicles/:id
  const deleteVehicleMatch = url.match(/^\/vehicles\/(\d+)$/);
  if (method === 'DELETE' && deleteVehicleMatch) {
    res.writeHead(204, {});
    res.end('');
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Mock route not defined', method, url }));
});

server.listen(PORT, () => console.log('Vehicle Service Mock running on port ' + PORT));
