import time


class SpeedEstimator:

    def __init__(self):

        self.previous_positions = {}
        self.vehicle_speeds = {}

        self.fps = 30


    def update(self, boxes):

        if boxes.id is None:
            return


        current_time = time.time()


        for box in boxes:


            track_id = int(box.id.item())


            x1, y1, x2, y2 = box.xyxy[0]


            center_x = int((x1+x2)/2)
            center_y = int((y1+y2)/2)



            if track_id in self.previous_positions:


                old_x, old_y, old_time = self.previous_positions[track_id]


                distance = (
                    ((center_x-old_x)**2 +
                    (center_y-old_y)**2)
                    **0.5
                )


                time_diff = current_time - old_time


                if time_diff > 0:

                    speed = (distance/time_diff) * 0.05

                    self.vehicle_speeds[track_id] = round(speed,2)



            self.previous_positions[track_id] = (
                center_x,
                center_y,
                current_time
            )



    def get_average_speed(self):

        if len(self.vehicle_speeds)==0:
            return 0

        return round(
            sum(self.vehicle_speeds.values()) /
            len(self.vehicle_speeds),
            2
        )



    def get_speed(self, track_id):

        return self.vehicle_speeds.get(track_id,0)