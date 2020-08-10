using UnityEngine;
using IronPython.Hosting;

namespace Exodrifter.UnityPython.Examples
{
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
			dynamic pytest = py.Test("by_excelsus");
			Debug.Log(pytest.display());
		}
	}
}