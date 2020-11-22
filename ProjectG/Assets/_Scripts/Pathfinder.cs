using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pathfinder : MonoBehaviour
{
	public Transform EndLocation;
	public float MoveSpeed;
	public int Interval;
	private Animator animator;
	private int CurrentNode;
	private List<Vector3> route;
	private DataConverter finder;
	private bool isMoving;

	// Start is called before the first frame update
	void Start()
    {
		animator = GetComponentInChildren<Animator>();
		finder = FindObjectOfType<DataConverter>();
		UpdateRoute();
    }

	private void UpdateRoute() {
		route = finder.GetRoute(transform.position, EndLocation.position);
		if (route.Count > 0) {
			CurrentNode = 0;
			isMoving = true;
		}
	}

	private void Update() {
		//Call this by interval system, probably yield the call to an interval distributer?
		//UpdateRoute
		if (isMoving) {
			MoveToward(GetCurrentTarget());
			CheckDistance();
		}
	}

	private Vector3 GetCurrentTarget() {
		return route[CurrentNode];
	}

	private void CheckDistance() {
		if (Vector3.Distance(transform.position, EndLocation.position) < float.Epsilon)
			Destroy(gameObject);
	}

	private void MoveToward(Vector3 target) {
		//Linear interpolation?
		transform.LookAt(target);
		//Vector3 movement = target - transform.localPosition;
		//transform.Translate( movement.normalized* MoveSpeed * Time.deltaTime);
		//Set the threashold so that it will not jiggle around next point forever
		float d = Vector3.Distance(transform.position, target);
		if(d < MoveSpeed * Time.deltaTime) {
			transform.position = target;
			++CurrentNode;
			if (CurrentNode >= route.Count)
				EndEvent();
		} else {
			transform.Translate(transform.forward * MoveSpeed * Time.deltaTime, Space.World);
			animator.SetFloat("Speed", MoveSpeed);
		}
	}

	private void EndEvent() {
		//This will be called when finder reaches the end point.
		//Probably play exit animation and then delete itself
		isMoving = false;
		animator.SetFloat("Speed", 0);
	}
}
