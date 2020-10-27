using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using IronPython.Hosting;

public class DataConverter : MonoBehaviour
{
	public string PythonScript;
	private dynamic PySolverClass;

	public ExitPointCollector ep;

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
		IList<float> ret = (IList<float>)PySolverClass.solve(a, b);
		List<Vector3> pars = new List<Vector3>();
		for(int idx = 0; idx < ret.Count; idx += 3) {
			pars.Add(new Vector3(ret[idx], ret[idx + 1], ret[idx + 2]));
		}
		return pars;
	}

	private float[] Digest(string a, Vector3 b, Vector3 c, Quaternion d) {
		float[] ret = new float[8];
		switch (a) {
		case "Wall":
			ret[0] = .0f;
			break;
		case "Road":
			ret[0] = 1.0f;
			break;
		case "Cross":
			ret[0] = 2.0f;
			break;
		default:
			ret[0] = .0f;
			break;
		}
		ret[1] = b.x;
		ret[2] = b.y;
		ret[3] = b.z;
		ret[4] = c.x;
		ret[5] = c.y;
		ret[6] = c.z;
		ret[7] = d.eulerAngles.y;
		return ret;
	}

	private string tString(float[] f) {
		StringBuilder sb = new StringBuilder();
		sb.Append("[ ");
		for(int i = 0; i < f.Length-1; i++) {
			sb.Append(f[i].ToString("F"));
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
		List<float> mapData = new List<float>(a.Length * 8);
		foreach (var b in a) {
			mapData.AddRange(Digest(b.tag, b.transform.position, b.transform.lossyScale, b.transform.rotation));
		}
		Debug.Log(tString(mapData.ToArray()));
		//Debug.Log(tString(ep.c.ToArray()));

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
		PySolverClass = py.TestAI(mapData, ep.c);
	}
}
