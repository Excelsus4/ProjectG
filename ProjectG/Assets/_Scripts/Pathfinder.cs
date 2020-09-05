using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pathfinder : MonoBehaviour
{
	public Vector3 EndLocation;
	public float MoveSpeed;
	public int Interval;
	private int CurrentNode;
	private List<Vector3> route;
	private DataConverter finder;

	// Start is called before the first frame update
	void Start()
    {
		finder = FindObjectOfType<DataConverter>();
		UpdateRoute();
    }

	private void UpdateRoute() {
		route = finder.GetRoute(transform.position, EndLocation);
		CurrentNode = 0;
	}

	private void Update() {
		//Call this by interval system, probably yield the call to an interval distributer?
		//UpdateRoute
		MoveToward(GetCurrentTarget());
	}

	private Vector3 GetCurrentTarget() {
		return route[CurrentNode];
	}

	private void MoveToward(Vector3 target) {
		//Linear interpolation?
		Vector3 movement = target - transform.localPosition;
		transform.Translate( movement.normalized* MoveSpeed * Time.deltaTime);
		//TODO: Rotate Model toward target
		//TODO: Set the threashold so that it will not jiggle around next point forever
	}

	private void EndEvent() {
		//TODO: This will be called when finder reaches the end point.
		//Probably play exit animation and then delete itself
	}
}
