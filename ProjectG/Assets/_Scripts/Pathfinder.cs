using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pathfinder : MonoBehaviour
{
	public Vector3 EndLocation;
	public float MoveSpeed;
	private int CurrentNode;

    // Start is called before the first frame update
    void Start()
    {
		DataConverter finder = FindObjectOfType<DataConverter>();
		List<Vector3> route = finder.GetRoute(transform.position, EndLocation);
		CurrentNode = 0;
		foreach(var a in route)
			Debug.Log(a);
    }
}
