using UnityEngine;
using IronPython.Hosting;
using System.Collections.Generic;

namespace Exodrifter.UnityPython.Examples
{
	public class MObject {
		public MObject(int type, Vector3 pos, Vector3 size, float rot) {
			this.type = type;
			data = new float[7];
			data[0] = pos.x;
			data[1] = pos.y;
			data[2] = pos.z;
			data[3] = size.x;
			data[4] = size.y;
			data[5] = size.z;
			data[6] = rot;
		}

		public int type;
		public float[] data;
	}

	public class PythonLibrary : MonoBehaviour
	{
		void Start()
		{
			var engine = Python.CreateEngine();
			var scope = engine.CreateScope();

			// Add the python library path to the engine. Note that this will
			// not work for builds; you will need to manually place the python
			// library files in a place that your code can find it at runtime.
			var paths = engine.GetSearchPaths();
			paths.Add(Application.dataPath + "/Python/Lib");
			engine.SetSearchPaths (paths);

			string code = @"
import os
filename = os.path.abspath ('PythonScripts/helloWorld.py');";

			var source = engine.CreateScriptSourceFromString(code);
			source.Execute(scope);

			dynamic py = engine.ExecuteFile(scope.GetVariable<string>("filename"));

			List<float> floatList = new List<float>();
			for(float i = 0; i < 16; i++) {
				floatList.Add(i);
			}
			dynamic pytest = py.Test(floatList);
			Debug.Log(pytest.display());
		}
	}
}