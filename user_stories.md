# User Stories
1. As an early-teens environmentalist, I want to look for beach cleanups with no minimum age requirement, so I can help clean up the environment too.
2. As a volunteer coordinator at a food bank, I want to be able to list full- and part-time opportunities separately, so I can separate volunteers based on available time commitments.
3. As a volunteer, I want to be able to update my contact info so that administrators know where to reach me.
4. As a nurse, I wanted to spend my free time helping older generations so that they feel appreciated and have a companion.
5. As a volunteer, I want to track my volunteer hours so that I can keep track of how much time I’ve spent.
6. As a skilled handyman, I wanted to spend time helping underprivileged communities with house needs, so that they can live under a comfortable roof.
7. As an elderly person, I want to filter volunteering events that are low-activity, so I can help with my limited mobility.
8. As a student, I want to find volunteer opportunities to help with gaining hours for volunteering, so I can go into the medical field.
9. As a student, I want an easy way to send my club administration proof of hours, so I can use the hours as credit for my requirement.
10. As a parent, I want a safe community to introduce my kids to volunteering and helping their community, so that they can build life skills and community involvement.
11. As a member of my community, I want to be able to volunteer for individuals that need extra care in groceries, so that my community has access to groceries.
12. As an organization lead, I want to be able to add volunteers to my organization, so that I can communicate directly with my volunteers.

# Exceptions
1. Time conflict: If a volunteer tries to enroll in an event that has a time conflict with another event they are already enrolled in, the scheduler will alert them of the time conflict and deny them from enrolling in the 2nd event.
2. Missing info: If a volunteer is missing necessary information to sign up for a certain event (e.g. phone number), the system will prompt the user to add the missing information.
3. Exceeds activity level: If a volunteer tries to enroll in an event that exceeds that volunteer’s previously indicated desired activity level (e.g. event is “high” activity: user indicated a desired “low” activity), the scheduler will warn them that the event is above their desired activity level. The user will be able to say “Never mind” and not enroll, or select “That’s okay” and enroll in the event.
4. Minimum number of volunteers: If the sign-up deadline for an event has passed and the number of registered volunteers is below the event publisher’s desired minimum number, the registrar will be notified. 
5. Invalid credentials for posting: If a company/person want to post a volunteer posting, they must have some sort of valid credentials otherwise they won’t be allowed to create a volunteer posting.
6. Maximum volunteer enrollment: If the max volunteer quota is filled, then volunteers can be added to an interest list; 24 hours before the event, if anyone drops, they will be added automatically. 
7. Cancelled event: If a user tries to sign up for an event that has been canceled, they will not be allowed to enroll in that event.
8. Excessive hours: If a user tries to log more hours than the event poster indicated were available for that event, the user will be notified and able to correct the hours or post anyway. 
9. Incorrect sign-up info: If a user fails to authenticate contact information (phone number, email) upon sign-up, the user will not be permitted to view or enroll in events until successful authentication is acheived.
10. Minimum age not met: If a volunteer tries to enroll in an event that has a minimum age requirement, and the volunteer is below the minimum age, the scheduler will not permit them to enroll in the event.
11. No results found: If there are no results based on the users search criteria, the user will be notified to broaden their search.
12. Bad content: If there is inappropriate content on the site (using a library of inappropriate words), it will be flagged for review and taken down.
