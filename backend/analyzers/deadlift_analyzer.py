import numpy as np
from typing import List, Dict
from models.analysis_result import AnalysisResult, FormIssue, CorrectiveExercise, Severity
from utils.pose_utils import (
    calculate_angle, get_landmark, PoseLandmark,
    calculate_vertical_alignment
)


class DeadliftAnalyzer:
    """Analyzer for deadlift form evaluation."""

    def __init__(self):
        self.corrective_exercises_db = {
            'rounded_back': CorrectiveExercise(
                name="Cat-Cow Stretch",
                description="On hands and knees, alternate between arching and rounding your back to improve spinal awareness.",
                sets="3",
                reps="10-12 cycles",
                focus="Improve spinal mobility and awareness of neutral spine"
            ),
            'hip_hinge': CorrectiveExercise(
                name="Romanian Deadlift (Light Weight)",
                description="Focus on hinging at hips while keeping knees slightly bent and back flat. Feel stretch in hamstrings.",
                sets="3",
                reps="10-12",
                focus="Master the hip hinge pattern fundamental to deadlifting"
            ),
            'core_bracing': CorrectiveExercise(
                name="Plank with Bracing",
                description="Hold plank position while practicing breathing and bracing your core. Breathe into your belly, not chest.",
                sets="3",
                reps="30-45 seconds",
                focus="Develop proper core bracing for spinal protection"
            ),
            'hamstring_flexibility': CorrectiveExercise(
                name="Standing Hamstring Stretch",
                description="Place foot on elevated surface, keep back straight, and lean forward from hips until stretch is felt.",
                sets="3",
                reps="30 seconds each leg",
                focus="Improve hamstring flexibility for better starting position"
            ),
            'lat_engagement': CorrectiveExercise(
                name="Lat Pull-downs with Focus",
                description="Pull bar down while focusing on 'pulling shoulders back and down' to engage lats.",
                sets="3",
                reps="12-15",
                focus="Strengthen lats and practice engagement for better bar path"
            ),
            'hip_mobility': CorrectiveExercise(
                name="Hip Flexor Stretch",
                description="Lunge position with back knee down. Push hips forward while keeping torso upright.",
                sets="3",
                reps="45 seconds each side",
                focus="Improve hip extension mobility"
            ),
            'glute_activation': CorrectiveExercise(
                name="Glute Bridges",
                description="Lie on back, feet flat, lift hips by squeezing glutes. Hold at top for 2 seconds.",
                sets="3",
                reps="15-20",
                focus="Activate glutes for proper hip drive in deadlift"
            ),
            'setup_practice': CorrectiveExercise(
                name="Deadlift Setup Drill (No Weight)",
                description="Practice setting up with perfect form: feet under hips, shins to bar, hinge at hips, grab bar, pull slack out, brace, lift.",
                sets="5",
                reps="5 repetitions",
                focus="Build muscle memory for proper deadlift setup"
            )
        }

    def analyze(self, poses: List[Dict]) -> AnalysisResult:
        """Analyze deadlift form from pose data."""
        issues = []
        recommendations = []
        corrective_exercises = []
        scores = []

        # Find key phases: starting position and lockout
        start_position = self._find_start_position(poses)
        lockout_position = self._find_lockout_position(poses)

        if not start_position or not lockout_position:
            return AnalysisResult(
                exercise="Deadlift",
                overall_score=0.0,
                issues=[FormIssue(
                    issue="No deadlift detected",
                    severity=Severity.CRITICAL,
                    description="Could not detect a complete deadlift movement in the video."
                )],
                recommendations=["Ensure the full deadlift movement from floor to lockout is visible"],
                corrective_exercises=[],
                summary="No valid deadlift movement detected.",
                frame_count=len(poses)
            )

        # Analyze various aspects of deadlift form
        back_issues, back_score = self._analyze_back_position(start_position, poses)
        issues.extend(back_issues)
        scores.append(back_score)

        hip_issues, hip_score = self._analyze_hip_position(start_position)
        issues.extend(hip_issues)
        scores.append(hip_score)

        bar_path_issues, bar_path_score = self._analyze_bar_path(poses)
        issues.extend(bar_path_issues)
        scores.append(bar_path_score)

        lockout_issues, lockout_score = self._analyze_lockout(lockout_position)
        issues.extend(lockout_issues)
        scores.append(lockout_score)

        setup_issues, setup_score = self._analyze_setup(start_position)
        issues.extend(setup_issues)
        scores.append(setup_score)

        # Calculate overall score
        overall_score = np.mean(scores) if scores else 0.0

        # Generate recommendations and corrective exercises
        recommendations = self._generate_recommendations(issues)
        corrective_exercises = self._get_corrective_exercises(issues)

        # Generate summary
        summary = self._generate_summary(overall_score, issues)

        return AnalysisResult(
            exercise="Deadlift",
            overall_score=round(overall_score, 2),
            issues=issues,
            recommendations=recommendations,
            corrective_exercises=corrective_exercises,
            summary=summary,
            frame_count=len(poses)
        )

    def _find_start_position(self, poses: List[Dict]) -> Dict:
        """Find the starting position (lowest hip position before lift)."""
        min_hip_height = float('inf')
        start_pose = None

        # Look at first third of the movement for starting position
        search_range = poses[:len(poses)//3] if len(poses) > 3 else poses

        for pose in search_range:
            left_hip = get_landmark(pose, PoseLandmark.LEFT_HIP)
            right_hip = get_landmark(pose, PoseLandmark.RIGHT_HIP)
            avg_hip_y = (left_hip['y'] + right_hip['y']) / 2

            if avg_hip_y > min_hip_height:  # Higher y = lower position
                min_hip_height = avg_hip_y
                start_pose = pose

        return start_pose

    def _find_lockout_position(self, poses: List[Dict]) -> Dict:
        """Find the lockout position (highest hip position)."""
        max_hip_height = float('-inf')
        lockout_pose = None

        # Look at last two thirds of the movement for lockout
        search_range = poses[len(poses)//3:] if len(poses) > 3 else poses

        for pose in search_range:
            left_hip = get_landmark(pose, PoseLandmark.LEFT_HIP)
            right_hip = get_landmark(pose, PoseLandmark.RIGHT_HIP)
            avg_hip_y = (left_hip['y'] + right_hip['y']) / 2

            if avg_hip_y < max_hip_height:  # Lower y = higher position
                max_hip_height = avg_hip_y
                lockout_pose = pose

        return lockout_pose

    def _analyze_back_position(self, start_position: Dict, all_poses: List[Dict]) -> tuple:
        """Analyze back position for rounding or hyperextension."""
        issues = []
        score = 100.0

        # Check multiple points in the lift for back rounding
        critical_poses = [start_position] + all_poses[::len(all_poses)//3][:2]

        for pose in critical_poses:
            left_shoulder = get_landmark(pose, PoseLandmark.LEFT_SHOULDER)
            left_hip = get_landmark(pose, PoseLandmark.LEFT_HIP)
            left_knee = get_landmark(pose, PoseLandmark.LEFT_KNEE)

            # Calculate back angle relative to vertical
            # A neutral spine should maintain consistent angle
            back_angle = calculate_angle(left_shoulder, left_hip, left_knee)

            # Check for rounded back (angle too acute)
            if back_angle < 130:
                severity = Severity.CRITICAL if back_angle < 120 else Severity.WARNING
                issues.append(FormIssue(
                    issue="Rounded Lower Back",
                    severity=severity,
                    description="Your lower back is rounding (flexion) during the lift. This is the most dangerous form error in deadlifts and can lead to serious injury. Keep your back flat and chest up.",
                    timestamp=pose['timestamp'],
                    frames=[pose['frame']]
                ))
                score -= 40 if severity == Severity.CRITICAL else 25
                break  # Only report once

        return issues, score

    def _analyze_hip_position(self, start_position: Dict) -> tuple:
        """Analyze hip starting position."""
        issues = []
        score = 100.0

        left_shoulder = get_landmark(start_position, PoseLandmark.LEFT_SHOULDER)
        left_hip = get_landmark(start_position, PoseLandmark.LEFT_HIP)
        left_knee = get_landmark(start_position, PoseLandmark.LEFT_KNEE)

        # Hip height relative to shoulders and knees
        # Hips should be between shoulders and knees
        if left_hip['y'] < left_shoulder['y']:
            issues.append(FormIssue(
                issue="Hips Starting Too High",
                severity=Severity.WARNING,
                description="Your hips are starting too high, turning this into more of a stiff-leg deadlift. Lower your hips slightly and ensure shoulders are over or slightly in front of the bar.",
                timestamp=start_position['timestamp'],
                frames=[start_position['frame']]
            ))
            score -= 20
        elif left_hip['y'] > left_knee['y']:
            issues.append(FormIssue(
                issue="Hips Starting Too Low",
                severity=Severity.WARNING,
                description="Your hips are starting too low, similar to a squat. This isn't efficient for deadlifting. Raise your hips slightly and focus on the hip hinge pattern.",
                timestamp=start_position['timestamp'],
                frames=[start_position['frame']]
            ))
            score -= 15

        return issues, score

    def _analyze_bar_path(self, poses: List[Dict]) -> tuple:
        """Analyze bar path - should be vertical and close to body."""
        issues = []
        score = 100.0

        # Track center point (approximating bar position)
        bar_positions = []

        for pose in poses:
            left_knee = get_landmark(pose, PoseLandmark.LEFT_KNEE)
            right_knee = get_landmark(pose, PoseLandmark.RIGHT_KNEE)
            # Approximate bar path using knee/shin position
            avg_x = (left_knee['x'] + right_knee['x']) / 2
            bar_positions.append(avg_x)

        # Check for horizontal deviation
        horizontal_range = max(bar_positions) - min(bar_positions)

        if horizontal_range > 0.08:
            issues.append(FormIssue(
                issue="Bar Path Not Vertical",
                severity=Severity.WARNING,
                description="The bar is drifting away from your body during the lift. Keep the bar close - it should travel in a straight vertical line. Engage your lats by 'pulling the bar into your shins'.",
                frames=list(range(len(poses)))
            ))
            score -= 20

        return issues, score

    def _analyze_lockout(self, lockout_position: Dict) -> tuple:
        """Analyze lockout position."""
        issues = []
        score = 100.0

        left_shoulder = get_landmark(lockout_position, PoseLandmark.LEFT_SHOULDER)
        left_hip = get_landmark(lockout_position, PoseLandmark.LEFT_HIP)
        left_knee = get_landmark(lockout_position, PoseLandmark.LEFT_KNEE)
        left_ankle = get_landmark(lockout_position, PoseLandmark.LEFT_ANKLE)

        # Check knee extension
        knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        if knee_angle < 170:
            issues.append(FormIssue(
                issue="Incomplete Knee Extension",
                severity=Severity.WARNING,
                description="Your knees are not fully extended at lockout. Squeeze your glutes and quads to fully extend your knees.",
                timestamp=lockout_position['timestamp'],
                frames=[lockout_position['frame']]
            ))
            score -= 15

        # Check for hyperextension of back
        hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)

        if hip_angle > 200:
            issues.append(FormIssue(
                issue="Lower Back Hyperextension",
                severity=Severity.WARNING,
                description="You're hyperextending (leaning back excessively) at lockout. Stand up straight with neutral spine - don't lean back.",
                timestamp=lockout_position['timestamp'],
                frames=[lockout_position['frame']]
            ))
            score -= 15

        return issues, score

    def _analyze_setup(self, start_position: Dict) -> tuple:
        """Analyze starting setup position."""
        issues = []
        score = 100.0

        left_shoulder = get_landmark(start_position, PoseLandmark.LEFT_SHOULDER)
        left_ankle = get_landmark(start_position, PoseLandmark.LEFT_ANKLE)

        # Shoulders should be over or slightly in front of the bar
        shoulder_bar_alignment = calculate_vertical_alignment(left_shoulder, left_ankle)

        if shoulder_bar_alignment > 0.15:
            issues.append(FormIssue(
                issue="Shoulders Too Far Behind Bar",
                severity=Severity.WARNING,
                description="Your shoulders should be over or slightly in front of the bar at the start. This helps maintain balance and proper bar path.",
                timestamp=start_position['timestamp'],
                frames=[start_position['frame']]
            ))
            score -= 10

        return issues, score

    def _generate_recommendations(self, issues: List[FormIssue]) -> List[str]:
        """Generate practical recommendations based on detected issues."""
        recommendations = []

        issue_types = {issue.issue for issue in issues}

        if "Rounded Lower Back" in issue_types:
            recommendations.append("PRIORITY: Fix your back rounding immediately. Reduce weight and focus on maintaining a neutral spine throughout the lift.")
            recommendations.append("Before each rep, take a deep breath into your belly, brace your core, and pull your chest up. Maintain this tension throughout.")
            recommendations.append("If you can't maintain a flat back, your hips may be too low or you may lack mobility. Work on hip hinge pattern and hamstring flexibility.")

        if "Hips Starting Too High" in issue_types:
            recommendations.append("Lower your hips slightly at the start. Your shoulders should be over or slightly ahead of the bar.")

        if "Hips Starting Too Low" in issue_types:
            recommendations.append("Raise your hips slightly. The deadlift is a hip hinge, not a squat. Your shins should be nearly vertical.")

        if "Bar Path Not Vertical" in issue_types:
            recommendations.append("Keep the bar close to your body throughout the lift. Think 'drag the bar up your shins and thighs'.")
            recommendations.append("Engage your lats by imagining you're 'bending the bar' or 'pushing the floor away' rather than pulling the bar up.")

        if "Incomplete Knee Extension" in issue_types:
            recommendations.append("Focus on fully locking out by squeezing glutes and quads at the top of the movement.")

        if "Lower Back Hyperextension" in issue_types:
            recommendations.append("Don't lean back at the top. Stand up straight with hips and knees fully extended, but maintain neutral spine.")

        if not recommendations:
            recommendations.append("Your form is solid! Continue focusing on maintaining this technique as you increase weight.")

        return recommendations

    def _get_corrective_exercises(self, issues: List[FormIssue]) -> List[CorrectiveExercise]:
        """Get corrective exercises based on detected issues."""
        exercises = []
        issue_types = {issue.issue for issue in issues}

        if "Rounded Lower Back" in issue_types:
            exercises.append(self.corrective_exercises_db['rounded_back'])
            exercises.append(self.corrective_exercises_db['core_bracing'])
            exercises.append(self.corrective_exercises_db['hamstring_flexibility'])

        if "Hips Starting Too High" in issue_types or "Hips Starting Too Low" in issue_types:
            exercises.append(self.corrective_exercises_db['hip_hinge'])
            exercises.append(self.corrective_exercises_db['setup_practice'])

        if "Bar Path Not Vertical" in issue_types:
            exercises.append(self.corrective_exercises_db['lat_engagement'])

        if "Incomplete Knee Extension" in issue_types:
            exercises.append(self.corrective_exercises_db['glute_activation'])

        if "Lower Back Hyperextension" in issue_types:
            exercises.append(self.corrective_exercises_db['core_bracing'])

        # Always include hip hinge practice for deadlifts
        if not exercises:
            exercises.append(self.corrective_exercises_db['hip_hinge'])

        return exercises

    def _generate_summary(self, overall_score: float, issues: List[FormIssue]) -> str:
        """Generate a summary of the analysis."""
        critical_issues = [i for i in issues if i.severity == Severity.CRITICAL]
        warning_issues = [i for i in issues if i.severity == Severity.WARNING]

        if overall_score >= 90:
            summary = "Excellent deadlift form! "
        elif overall_score >= 75:
            summary = "Good deadlift technique with minor areas for improvement. "
        elif overall_score >= 60:
            summary = "Decent form, but several areas need attention. "
        else:
            summary = "Significant form issues detected that require immediate attention. "

        if critical_issues:
            summary += f"CRITICAL: Address {len(critical_issues)} critical issue(s) immediately to prevent injury. "

        if warning_issues:
            summary += f"Work on {len(warning_issues)} technique adjustment(s) to optimize your deadlift."

        return summary
