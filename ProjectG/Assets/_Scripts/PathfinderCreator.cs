using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PathfinderCreator : MonoBehaviour
{
	public GameObject PathfinderPrefab;
	public ExitPointCollector ExitPoints;

	private bool isFindingPosition;
	private bool singleTickWaiter;
	private int RoadCounter;
	private int WallCounter;

	private void Awake() {
		RoadCounter = 0;
		WallCounter = 0;
		isFindingPosition = false;
		singleTickWaiter = false;
	}

	public void CreateNewPathfinder() {
		if (!isFindingPosition) {
			transform.SetPositionAndRotation(new Vector3(Random.Range(-100, 100), 0, Random.Range(-100, 100)), Quaternion.identity);
			isFindingPosition = true;
		}
	}

	private void ActuallyInstantiate() {
		GameObject pathfinder = Instantiate(PathfinderPrefab, transform.position, Quaternion.Euler(0, Random.Range(0,360), 0));
		Pathfinder script = pathfinder.GetComponent<Pathfinder>();
		script.EndLocation = ExitPoints.t[Random.Range(0, ExitPoints.t.Count)];
	}

	private void FixedUpdate() {
		if (isFindingPosition && singleTickWaiter) {
			if(RoadCounter > 0 && WallCounter <= 0) {
				ActuallyInstantiate();
				isFindingPosition = false;
				singleTickWaiter = false;
			} else {
				transform.SetPositionAndRotation(new Vector3(Random.Range(-100, 100), 0, Random.Range(-100, 100)), Quaternion.identity);
			}
		}else if (isFindingPosition) {
			singleTickWaiter = true;
		}
	}

	private void OnTriggerEnter(Collider other) {
		switch (other.tag) {
		case "Road":
			RoadCounter++;
			break;
		case "Wall":
			WallCounter++;
			break;
		}
	}

	private void OnTriggerExit(Collider other) {
		switch (other.tag) {
		case "Road":
			RoadCounter--;
			break;
		case "Wall":
			WallCounter--;
			break;
		}
	}
}
