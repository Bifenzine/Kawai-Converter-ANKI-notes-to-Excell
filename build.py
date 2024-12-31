import PyInstaller.__main__
import os
import sys

def build_exe():
    """
    Build the executable with PyInstaller, including all necessary dependencies
    """
    options = [
        'kawaii_converter.py',  # Your main Python script
        '--onefile',  # Create a single executable
        '--icon=jelly.ico',  # Commented out icon for now
        '--windowed',  # Use the windowed subsystem (no console)
        '--name=KawaiiConverter',
        '--clean',  # Clean PyInstaller cache
        '--add-data=requirements.txt;.',
        # Hidden imports for pandas and other libraries
        '--hidden-import=pandas',
        '--hidden-import=pandas.plotting',
        '--hidden-import=pandas.core.algorithms',
        '--hidden-import=pandas.core.arrays',
        '--hidden-import=pandas.core.computation.expressions',
        '--hidden-import=pandas.core.indexes.numeric',
        '--hidden-import=pandas.core.dtypes.common',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.ttk',
        # Excluding unnecessary packages to reduce size
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=numpy.random._examples',
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.'
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(options)

if __name__ == '__main__':
    try:
        build_exe()
        print("Build completed successfully!")
    except Exception as e:
        print(f"Build failed with error: {str(e)}")
        sys.exit(1)