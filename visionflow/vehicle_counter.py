class VehicleCounter:
    def __init__(self):

        # Store unique vehicle IDs
        self.vehicle_ids = set()

        # Vehicle category counts

        self.vehicle_counts = {"car": 0, "bus": 0, "truck": 0, "motorcycle": 0, "bicycle": 0}

    def update(self, boxes, names):

        if boxes.id is None:
            return

        ids = boxes.id.cpu().numpy()

        classes = boxes.cls.cpu().numpy()

        for track_id, cls_id in zip(ids, classes):
            track_id = int(track_id)

            class_name = names[int(cls_id)]

            # Count only new vehicles

            if track_id not in self.vehicle_ids:
                self.vehicle_ids.add(track_id)

                if class_name in self.vehicle_counts:
                    self.vehicle_counts[class_name] += 1

    def get_count(self):

        return len(self.vehicle_ids)

    def get_details(self):

        return self.vehicle_counts
