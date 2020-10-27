using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExitPointCollector : MonoBehaviour {
	public List<float> c;
	public List<Vector3> p;

	private void Awake() {
		c = new List<float>();
		p = new List<Vector3>();
		var a = GetComponentsInChildren<MeshRenderer>();
		foreach(var b in a) {
			p.Add(b.transform.position);
			c.Add(b.transform.position.x);
			c.Add(b.transform.position.y);
			c.Add(b.transform.position.z);
		}

		//print(c);
	}
}
