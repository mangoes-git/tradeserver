import shelve


class TrackID:
    current_id: int
    shelf = None

    def __init__(self):
        self.shelf = shelve.open("./track_order_id/order_id.db", writeback=True)
        if "id" in self.shelf:
            self.current_id = self.shelf["id"]
            return
        self.current_id = 0
        self.shelf["id"] = self.current_id

    def get_next(self):
        self.current_id += 1
        self.shelf["id"] = self.current_id
        return self.current_id

    def close(self):
        self.shelf.close()
