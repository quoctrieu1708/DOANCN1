package com.example.backend.service;

import com.example.backend.entity.Attendance;
import com.example.backend.entity.User;
import com.example.backend.repository.AttendanceRepository;
import com.example.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDate;
import java.time.LocalTime;

@Service
public class AttendanceService {

    @Autowired
    private PythonIntegrationService pythonIntegrationService;

    @Autowired
    private AttendanceRepository attendanceRepository;

    @Autowired
    private UserRepository userRepository;

    public String checkIn(MultipartFile image) throws IOException {
        // 1. Send image to Python service to recognize
        Long userId = pythonIntegrationService.recognizeFace(image);

        if (userId == null) {
            throw new RuntimeException("Face not recognized or unknown user.");
        }

        // 2. Prevent duplicate check-in today
        LocalDate today = LocalDate.now();
        if (attendanceRepository.existsByUserIdAndDate(userId, today)) {
            throw new RuntimeException("User already checked in today.");
        }

        // 3. Save attendance
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Attendance attendance = Attendance.builder()
                .user(user)
                .date(today)
                .checkInTime(LocalTime.now())
                .build();

        attendanceRepository.save(attendance);

        return "Check-in successful for " + user.getName();
    }
}
