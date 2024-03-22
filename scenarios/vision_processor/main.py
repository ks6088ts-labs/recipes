import cv2 as cv
import typer
from dotenv import load_dotenv

app = typer.Typer()

class FpsCalculator:
    def __init__(self):
        self._tm = cv.TickMeter()
        self._tm.start()
        self._count = 0
        self._max_count = 10
        self._fps = 0

    def update(self)->float:
        if self._count == self._max_count:
            self._tm.stop()
            self._fps = self._max_count / self._tm.getTimeSec()
            self._tm.reset()
            self._tm.start()
            self._count = 0
        self._count += 1
        return self._fps

@app.command()
def run(
    settings: str = typer.Option("settings.env", help="Settings file"),
    video: int = typer.Option(0, help="Video source"),
):
    load_dotenv("settings.env")

    cap = cv.VideoCapture(int(video))
    fps_calculator = FpsCalculator()

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        fps = fps_calculator.update()
        cv.putText(frame, 'FPS: {:.2f}'.format(fps),
                    (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Our operations on the frame come here
        # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv.imshow("frame", frame)

        if cv.waitKey(1) == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    app()
