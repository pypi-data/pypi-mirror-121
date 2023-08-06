class HandlerBackend(object):
    def __init__(self, handlers=None):
        if handlers is None:
            handlers = {}
            
        self.handlers = handlers
    
    def register_handler(self, peer_id, handler):
        if peer_id in self.handlers:
            self.handlers[peer_id].append(handler)
        else:
            self.handlers[peer_id] = [handler]
            
    def get_handlers(self, peer_id):
            return self.handlers.pop(peer_id, None)
            