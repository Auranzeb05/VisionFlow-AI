class WrongWayDetector:
    def __init__(self):
        self.previous_positions = {}
        self.frames_seen = {}

    def check(self, boxes):

        wrong_way_ids = []

        for box in boxes:
            if box.id is None:
                continue

            track_id = int(box.id.item())

            x1, y1, x2, y2 = box.xyxy[0]

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # First time seeing vehicle
            if track_id not in self.previous_positions:
                self.previous_positions[track_id] = (center_x, center_y)

                self.frames_seen[track_id] = 0

                continue

            old_x, old_y = self.previous_positions[track_id]

            movement_x = center_x - old_x
            center_y - old_y

            self.frames_seen[track_id] += 1

            # Ignore vehicles for first few frames
            if self.frames_seen[track_id] < 10:
                self.previous_positions[track_id] = (center_x, center_y)

                continue

            # Change this depending on traffic direction

            # Vehicles normally moving LEFT -> RIGHT
            if movement_x < -8:
                wrong_way_ids.append(track_id)

            self.previous_positions[track_id] = (center_x, center_y)

        return wrong_way_ids
