Medical reservation system
==========================
Simple system for making reservations and display timetables.

Requirement
-----------
 - django 1.3+

Users actions
-------------

### Unauthorized user (patient)
 - select date and time of visit reservation and book for it if it is empty

### Authorized user (nurse etc.)
 - same as unauthorized user
 - can see visit reservation status
 - can see name of patient on booked reservation
 - can book patient on "authorized only" reservation
 - click on reservation hold it
 - unbook patient
 - unhold reservation
 - print simple and detail reservation list for selected day

### Staff user (administrator)
 - enable/disable reservation
 - has access to adminstration page
