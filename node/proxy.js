const { Client } = require('express-websocket-proxy')
const axios = require("axios")

const proxyClient = new Client('wss://proxy.oyintare.dev/')

async function ProxyRequest(req) {
	const result = await axios({
		method: req.method.toLowerCase(),
		url: `http://localhost:8097${req.originalUrl.substring("/nlu".length)}`,
		body: req.body,
		headers: req.headers,
		validateStatus: () => true,
	})

	req.sendBody(result.data)
}

proxyClient.on('-get|nlu.*', ProxyRequest)
proxyClient.on('-post|nlu.*', ProxyRequest)
proxyClient.on('-put|nlu.*', ProxyRequest)
proxyClient.on('-delete|nlu.*', ProxyRequest)

proxyClient.connect()