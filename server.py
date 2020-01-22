class Socket():
	
		def __init__(self, client_handler):
				self.client_handler = client_handler
			
				ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
				ssl_context.load_cert_chain("ssl/cert.pem", "ssl/key.pem")

				start_server = websockets.serve(
						self.socket_handler, "0.0.0.0", 443, ssl=ssl_context
				)
				
				try:
						asyncio.get_event_loop().run_until_complete(start_server)
						asyncio.get_event_loop().run_forever()
				except KeyboardInterrupt:
						print("Ending program...")

						
		async def socket_handler(self, websocket, path):
				client = self.client_handler.add_client(websocket)
				while True:
						message = await websocket.recv()
						
						await self.client_handler.process_message_received(websocket, message)
						
						
						queue = client.get_queue_and_clear()
						
						client.run_loop()
						
						for message in queue:
								await websocket.send(message)
														
								
						
client_handler = ClientHandler()					
socket = Socket(client_handler)			
