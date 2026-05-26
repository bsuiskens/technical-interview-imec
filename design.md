The requirement list has been interpreted as a request for a urgently needed Proof-of-Concept. 

This would give preference to minimal-setup, low-configuration frameworks with a low level of commitment required, that can be easily taken out and replaced with more extensible or performant solutions.

The project will be initialized using a practice project I've made as its base to touch up on the technologies picked, in order to quickly sort out the basics.

Key technologies chosen:

REST Layer: FastAPI + Pydantic; Wide familiarity, minimal configuration, and business logic will remain framework-agnostic and isolated from HTTP concerns, allowing future migration to different API frameworks if needed.

Database layer: RDBMS (SQL) + SQLAlchemy; Data structure present in excel sheet strongly implies relational bonds , so SQL will be preferred. For the proof of concept, 
this app will initially feature a SQLite serverless database in order to further bring down the setup burden, as SQLAlchemy and Python come build-in with the SQLite driver. SQLite is of course not suited for most production projects, so if I still have adequate time we shall default to the axiom of Just Use Postgres and replace it with a containerized Postgres instance. The schema will consists out of 4 tables handling the different objects described in the excel sheet (activities, exchanges, material impacts and electricity impacts); partner data can for the time being be managed with a simple text field on activities that shares the unique constraint with the activity name.

Excel input handling: pandas + openpyxl; standard strategy for excel handling.

Testing strategy: Basic tests for the recursive calculation will be implemented in pytest if time is available.

Why not the BW2 package?: As the document specifies that it is a simplified BW2 datastructure, this implies the PoC is not required to have outright BW2 compatability and may in fact not operate with the example file. On top of BW2 being rather heavyweight and high-configuration, I've elected to forgo it for the time being.
