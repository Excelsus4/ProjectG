﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using IronPython.Hosting;

public class DataConverter : MonoBehaviour
{
	public string PythonScript;
	private dynamic PySolverClass;

	public ExitPointCollector ep;
	public bool UnityDebugMode;
	
	public List<Vector3> GetRoute(Vector3 p1, Vector3 p2) {
		List<float> a, b;
		a = new List<float>(3);
		a.Add(p1.x);
		a.Add(p1.y);
		a.Add(p1.z);
		b = new List<float>(3);
		b.Add(p2.x);
		b.Add(p2.y);
		b.Add(p2.z);
		Debug.Log("GetRoute");
		Debug.Log(tString(a.ToArray(), 3));
		Debug.Log(tString(b.ToArray(), 3));
		dynamic retd = PySolverClass.solve(a, b);
		IList<object> ret = (IList<object>)retd;
		List<Vector3> pars = new List<Vector3>();
		for(int idx = 0; idx < ret.Count; idx += 3) {
			pars.Add(new Vector3(System.Convert.ToSingle((double)ret[idx]), System.Convert.ToSingle((double)ret[idx + 1]), System.Convert.ToSingle((double)ret[idx + 2])));
		}
		return pars;
	}

	private float[] Digest(string a, Vector3 b, Vector3 c, Quaternion d) {
		float[] ret = new float[8];
		ret[1] = b.x;
		ret[2] = b.y;
		ret[3] = b.z;
		ret[4] = c.x;
		ret[5] = c.y;
		ret[6] = c.z;
		switch (a) {
		case "Wall":
			ret[0] = .0f;
			break;
		case "Road":
			ret[0] = 1.0f;
			break;
		case "Cross":
			ret[0] = 2.0f;
			ret[4] *= 10;
			ret[5] *= 10;
			ret[6] *= 10;
			break;
		default:
			ret[0] = .0f;
			break;
		}
		ret[7] = d.eulerAngles.y;
		return ret;
	}

	private string tString(float[] f, int cut) {
		StringBuilder sb = new StringBuilder();
		sb.Append("[ ");
		for(int i = 0; i < f.Length-1; i++) {
			sb.Append(f[i].ToString("F"));
			if ((i+1) % cut == 0)
				sb.Append("\n");
			else
				sb.Append(" , ");
		}
		sb.Append(f[f.Length - 1].ToString("F"));
		sb.Append(" ]");
		return sb.ToString();
	}
	
	private void Awake() {
		PySolverClass = null;
		// ==========================================
		// Converting Map into float List
		var a = GetComponentsInChildren<BoxCollider>();
		var b = GetComponentsInChildren<MeshCollider>();

		List<float> mapData = new List<float>((a.Length + b.Length) * 8);

		foreach (var t in b) {
			mapData.AddRange(Digest(t.tag, t.transform.position, t.transform.lossyScale, t.transform.rotation));
		}

		foreach (var t in a) {
			if(t.tag != "Wall")
				mapData.AddRange(Digest(t.tag, t.transform.position, t.transform.lossyScale, t.transform.rotation));
		}

		foreach (var t in a) {
			if (t.tag == "Wall")
				mapData.AddRange(Digest(t.tag, t.transform.position, t.transform.lossyScale, t.transform.rotation));
		}

		Debug.Log(tString(mapData.ToArray(), 8));
		Debug.Log(tString(ep.c.ToArray(), 3));

		// ==========================================
		// Python Engine
		var engine = Python.CreateEngine();
		var scope = engine.CreateScope();

		// Add the python library path to the engine. Note that this will
		// not work for builds; you will need to manually place the python
		// library files in a place that your code can find it at runtime.
		var paths = engine.GetSearchPaths();
		paths.Add(Application.dataPath + "/Python/Lib");
		engine.SetSearchPaths(paths);

		string code = @"
import os
filename = os.path.abspath ('PythonScripts/"+PythonScript+"');";

		var source = engine.CreateScriptSourceFromString(code);
		source.Execute(scope);

		dynamic py = engine.ExecuteFile(scope.GetVariable<string>("filename"));


		// 1. mapData
		// 2. ep.c
		if(!UnityDebugMode)
			PySolverClass = py.TestAI(mapData, ep.c);
	}

	public void ManualTrain() {
		PySolverClass.QLTrain();
	}
}
