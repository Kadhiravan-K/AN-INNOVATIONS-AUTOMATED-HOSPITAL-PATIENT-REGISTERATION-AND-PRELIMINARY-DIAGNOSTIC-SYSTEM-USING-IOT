# PROVISIONAL SPECIFICATION

(Under Section 10 of the Patents Act, 1970)

**AN AUTOMATED HOSPITAL PATIENT REGISTRATION AND PRELIMINARY DIAGNOSTIC SYSTEM USING IOT-BASED SENSORS**

## A. Title of the Invention:

The present invention relates to an intelligent hospital patient registration system designed to streamline and automate the patient onboarding process. The system utilizes a single touchscreen interface through which patients can register themselves by selecting appropriate options such as permanent or temporary registration. It incorporates digital identity verification, enabling secure authentication using Aadhaar-based OTP validation.

The system is further integrated with multiple sensors to perform preliminary health assessments, including body temperature, heart rate, and environmental parameters. These sensor readings are automatically captured and linked to the respective patient’s registration profile in real time. Based on the patient’s input symptoms and collected health data, the system performs an initial analysis and assists in assigning the appropriate department and medical specialist.

Upon completion, the system generates a unique token along with a summarized patient report containing personal details, measured health parameters, and preliminary analysis. This information is made available for both the patient and the healthcare provider, thereby reducing manual workload, minimizing waiting time, and improving overall efficiency in hospital operations. The invention provides a compact, cost-effective, and user-friendly solution for modern healthcare environments.

## B. Field of the Invention:

The present invention relates to the field of healthcare technology, particularly to systems and methods for automating patient registration and preliminary health assessment in medical facilities. More specifically, the invention pertains to an intelligent hospital patient registration system that integrates digital identity verification, embedded sensor-based health monitoring, and an interactive touchscreen interface for efficient patient onboarding.

The invention falls within the interdisciplinary domains of Internet of Things (IoT)-enabled medical systems, embedded system design, human–machine interaction, and digital healthcare infrastructure. It involves the use of connected sensors for measuring vital health parameters such as body temperature and heart rate, along with software-driven data processing and storage mechanisms for maintaining patient records.

Furthermore, the invention is related to smart healthcare kiosk systems that facilitate self-service patient interaction, reduce dependency on manual registration processes, and enhance operational efficiency in hospitals and clinics. It also encompasses secure digital authentication mechanisms, such as Aadhaar-based verification, to ensure accurate patient identification and data integrity.

The system is designed to support real-time data acquisition, automated decision-making for department allocation, and generation of patient-specific tokens and summaries, thereby contributing to improved workflow management and enhanced quality of care in modern healthcare environments.

## C. Background of the Invention:

In modern healthcare systems, patient registration is a critical initial step that significantly influences the efficiency of hospital operations and the quality of patient care. Conventional patient registration processes are largely manual, requiring patients to fill out forms and wait in queues, which often leads to delays, data entry errors, and increased workload for hospital staff. These inefficiencies become more pronounced in high-volume healthcare facilities where managing patient flow is a major challenge.

Existing digital registration systems, although an improvement over manual methods, are often limited in functionality. Most systems focus only on collecting basic patient information and do not incorporate real-time health assessment or intelligent decision-making capabilities. As a result, patients are still required to undergo separate preliminary checkups, leading to additional waiting time and fragmented workflows.

Furthermore, current systems lack integration with secure identity verification mechanisms, which can result in inaccuracies in patient data and difficulties in retrieving medical history. In regions where digital identity systems such as Aadhaar are available, there is an opportunity to enhance registration accuracy and streamline patient identification, but such integration is not widely implemented in existing solutions.

Another limitation of traditional approaches is the absence of automated triage or department allocation. Patients are often required to manually select departments or rely on staff assistance, which may not always be accurate, especially when symptoms are unclear. This can lead to inefficient routing, overcrowding in certain departments, and delays in receiving appropriate medical attention.

Additionally, preliminary health assessments such as temperature and heart rate measurement are typically conducted separately by medical personnel, increasing the burden on healthcare workers and slowing down the overall process. The lack of an integrated system that combines registration, identity verification, vital sign monitoring, and initial analysis highlights a significant gap in current healthcare infrastructure.

Therefore, there exists a need for an intelligent, automated, and integrated patient registration system that can streamline the entire process, reduce manual intervention, improve accuracy, and enhance the overall efficiency of healthcare service delivery.

## D. Objectives of the Invention:

- The primary objective of the present invention is to provide an intelligent and automated hospital patient registration system that simplifies and enhances the efficiency of the patient onboarding process through a single interactive interface.
- Another objective of the invention is to eliminate manual registration procedures by enabling patients to self-register using a user-friendly touchscreen system, thereby reducing waiting time, minimizing human errors, and decreasing the workload on hospital staff.
- A further objective of the invention is to integrate secure digital identity verification, such as Aadhaar-based authentication, to ensure accurate patient identification and facilitate reliable retrieval of medical records.
- An additional objective is to incorporate embedded sensor-based health monitoring to automatically measure vital parameters, including body temperature and heart rate, during the registration process, thereby enabling preliminary health assessment without the need for separate medical intervention.
- Another objective of the invention is to provide an intelligent system capable of analyzing patient inputs and basic health data to assist in automatic department allocation and preliminary triage, ensuring that patients are directed to the appropriate medical specialist efficiently.
- It is also an objective of the invention to generate a unique registration token along with a comprehensive patient summary, including personal details, recorded health parameters, and symptom-based analysis, to assist healthcare professionals during consultation.
- A further objective is to design a compact, cost-effective, and scalable system that can be easily deployed in hospitals, clinics, and other healthcare facilities, improving overall operational workflow and patient experience.
- Finally, the invention aims to contribute to the advancement of smart healthcare infrastructure by integrating IoT, embedded systems, and digital technologies into a unified platform for efficient and reliable patient management.

## E. Summary of the Invention:

The present invention provides an intelligent hospital patient registration system that integrates patient identification, automated data collection, sensor-based health monitoring, and preliminary analysis into a unified platform. The system is designed as a single-interface, touchscreen-based solution that enables patients to self-register in a simple and efficient manner.

In one embodiment, the system allows patients to select between permanent and temporary registration modes. For permanent registration, secure digital identity verification is performed using Aadhaar-based authentication with OTP validation, ensuring accurate patient identification and seamless retrieval of medical history. Temporary registration provides a privacy-focused alternative for patients who choose not to disclose their identity.

The invention further incorporates embedded sensors to measure vital health parameters such as body temperature and heart rate during the registration process. These measurements are automatically captured and linked to the patient’s profile in real time. The system may also collect additional environmental data to support contextual health analysis.

Based on the patient’s input symptoms and recorded parameters, the system performs a preliminary analysis and assists in determining the appropriate medical department and specialist. This automated triage functionality enhances patient routing and reduces dependency on manual intervention.

Upon completion of the registration process, the system generates a unique token along with a detailed patient summary that includes identification details, health parameters, symptom analysis, and department allocation. This information is made readily available for healthcare providers, facilitating faster and more informed medical consultations.

Overall, the invention offers a compact, efficient, and cost-effective solution that improves patient flow, reduces waiting time, enhances data accuracy, and supports modern healthcare automation.

## F. Detailed Description of the Invention:

The present invention relates to an intelligent hospital patient registration system designed to automate and streamline the patient onboarding process using a single touchscreen-based interface integrated with sensor-based health monitoring and digital identity verification.

In a preferred embodiment, the system comprises a processing unit, such as a Raspberry Pi, operatively connected to a touchscreen display that serves as the primary user interface. The system further includes embedded sensors for measuring vital health parameters, communication modules for network connectivity, and an output module for generating patient tokens and summaries.

The operation of the system begins with the activation of the registration interface, which displays a user-friendly graphical interface on the touchscreen. The patient initiates the process by selecting a registration option, wherein the system provides a choice between a permanent registration mode and a temporary registration mode. The permanent mode enables storage and retrieval of patient medical history, while the temporary mode allows limited and privacy-focused registration without long-term data retention.

In the case of permanent registration, the system prompts the user to enter a digital identity number, such as an Aadhaar number. Upon submission, the system initiates a secure authentication process by sending a one-time password (OTP) to the registered mobile number associated with the identity. The user enters the received OTP, and upon successful verification, the system retrieves and displays the patient’s basic identity details for confirmation. The user may confirm whether the registration is for themselves or on behalf of another individual, and the system proceeds accordingly.

Following identity confirmation, the system guides the user to select the type of visit, such as outpatient consultation or recheckup. The user is then prompted to input symptoms or the reason for the visit through predefined options or interactive input fields. Based on the provided information, the system employs predefined logic or algorithmic processing to determine the appropriate medical department and relevant specialist for consultation.

Subsequently, the system initiates a smart health checkup phase, wherein embedded sensors are activated to measure vital parameters. A non-contact infrared temperature sensor is used to measure the patient’s body temperature, while a pulse sensor is utilized to detect heart rate. Environmental sensors may also capture ambient parameters such as temperature, humidity, and pressure for contextual analysis. The system ensures that sensor readings are taken only when valid input conditions are met, such as proper finger placement or appropriate proximity to the sensor. Multiple readings may be captured and averaged to improve accuracy.

All acquired sensor data is processed in real time and associated with a unique patient identification number generated at the start of the registration process. The system maintains a structured data record that includes patient details, measured health parameters, symptom inputs, and timestamp information. This data is stored locally or in a connected database for further use.

The system then proceeds to a symptom analysis stage, where it presents a set of guided diagnostic questions to the patient. Based on the responses, the system performs a preliminary assessment to assist healthcare providers in understanding the patient’s condition prior to consultation.

Upon completion of all steps, the system generates a unique registration token containing details such as token number, assigned department, doctor or specialist type, and room information. Additionally, a comprehensive patient summary is generated, which includes identity details, recorded vital parameters, symptom description, and preliminary analysis. This information may be displayed on the screen and optionally printed using a connected thermal printer.

The system is further designed to include alert mechanisms such as buzzers or visual indicators to guide the user during various stages of the process, including successful input, errors, or completion of measurements. The interface may also incorporate timeout and reset functions to ensure smooth operation and readiness for the next patient.

Overall, the invention provides a fully integrated, automated, and user-friendly solution for hospital patient registration, combining identity verification, health monitoring, and intelligent routing into a single cohesive system.

## G. Advantages of the Invention:

The present invention offers several significant advantages over conventional patient registration systems and existing digital solutions:

- **Automation:** The automation of the patient registration process through a single interactive touchscreen interface eliminates the need for manual form filling and reduces dependency on hospital staff, leading to faster onboarding and better operational efficiency.
- **Digital Identity Verification:** Integration of digital identity verification, such as Aadhaar-based authentication, ensures accurate patient identification, minimizes manual data entry errors, and facilitates easy retrieval of patient history.
- **Real-Time Health Monitoring:** Embedded sensors measure vital parameters such as body temperature and heart rate on the spot. This eliminates separate preliminary checkups and reduces workload on healthcare personnel.
- **Intelligent Triage:** The intelligent analysis of patient symptoms and collected data enables automated department allocation and preliminary triage, directing patients to the appropriate medical specialist efficiently.
- **Patient Experience:** The system enhances patient experience by offering a user-friendly, guided interface. Both permanent and temporary registration options provide flexibility and respect privacy preferences.
- **Comprehensive Patient Summary:** Generation of a comprehensive patient summary and a unique registration token supports healthcare providers in making quicker and more informed decisions during consultation.
- **Cost-effective and Scalable:** The invention is compact, cost-effective, and scalable, suitable for deployment in various healthcare facilities. Its modular design allows easy integration of new features.
- **Smart Healthcare Infrastructure:** The system merges IoT, embedded systems, and digital technologies into a unified platform, improving efficiency, accuracy, and overall patient management.

## H. Prototype Development and Bill of Materials

The prototype of the proposed intelligent hospital patient registration system is developed using a compact embedded platform centered around a Raspberry Pi 4, which functions as the main processing and control unit. The Raspberry Pi is interfaced with a 7-inch touchscreen display that serves as the primary user interface for both patient interaction and system control.

The system software is designed to provide a guided, step-by-step registration process, including token selection, identity verification, symptom input, and health parameter measurement. The graphical user interface (GUI) is developed to be intuitive and user-friendly, ensuring ease of use for patients with minimal technical knowledge.

Multiple sensors are integrated with the Raspberry Pi through communication protocols such as I2C and GPIO. A non-contact infrared temperature sensor (MLX90614) is used for measuring body temperature, while a pulse sensor (KY-039) is used to detect heart rate. Additionally, a BME280 sensor is incorporated to measure environmental parameters such as temperature, humidity, and atmospheric pressure.

A touch sensor module is used as an auxiliary input device to trigger specific actions such as starting measurements or confirming inputs. A buzzer is included to provide audio feedback during different stages of the process, such as successful input, errors, or completion of measurements.

The system is programmed to collect sensor data only when valid conditions are detected, such as proper finger placement for heart rate measurement or appropriate proximity for temperature sensing. The acquired data is processed in real time and linked to a unique patient identification number generated during registration.

All patient data, including identity details, sensor readings, and symptom inputs, are stored in a local database within the Raspberry Pi. Upon completion of the registration process, the system generates a patient summary and token, which can be displayed on the screen or printed using an optional thermal printer.

The entire system is assembled within a compact enclosure designed as a kiosk, ensuring proper placement of sensors, display, and input modules for convenient patient interaction. The prototype is powered using a regulated power supply to ensure stable operation.

### Bill of Materials:

| Sl. No. | Component Name              | Specification / Description              | Quantity |
| ------- | --------------------------- | ---------------------------------------- | -------- |
| 1       | Raspberry Pi 4 Model B      | 4GB/8GB RAM, main processing unit        | 1        |
| 2       | MicroSD Card                | 32GB or higher (for OS and data storage) | 1        |
| 3       | 7-inch Touchscreen Display  | HDMI/DSI compatible with Raspberry Pi    | 1        |
| 4       | Power Adapter               | 5V, 3A supply for Raspberry Pi           | 1        |
| 5       | BME280 Sensor Module        | Temperature, humidity, pressure sensor   | 1        |
| 6       | MLX90614 (GY-906) IR Sensor | Non-contact body temperature sensor      | 1        |
| 7       | KY-039 Pulse Sensor         | Heart rate measurement sensor            | 1        |
| 8       | Touch Sensor (TTP223)       | Capacitive touch input module            | 1        |
| 9       | Buzzer Module               | Audio alert component                    | 1        |
| 10      | Jumper Wires                | Male-to-male / male-to-female connectors | As req.  |
| 11      | Breadboard / PCB            | Circuit prototyping and connections      | 1        |
| 12      | Enclosure / Kiosk Frame     | Mechanical housing for system            | 1        |



## K. Declaration:

The inventors declare that the information presented in this provisional specification is original and unpublished. This submission is made to claim priority rights under the Indian Patents Act, 1970.
