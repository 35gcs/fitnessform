import numpy as np
from typing import List, Dict
from models.analysis_result import AnalysisResult, FormIssue, CorrectiveExercise, Severity
from utils.pose_utils import (
    calculate_angle, get_landmark, PoseLandmark,
    calculate_vertical_alignment, calculate_depth_ratio
)


class SquatAnalyzer:
    """Analyzer for squat form evaluation."""

    def __init__(self):
        self.corrective_exercises_db = {
            'knee_valgus': CorrectiveExercise(
                name="Banded Lateral Walks",
                description="Place a resistance band around your knees. Step laterally while maintaining tension, keeping knees pushed outward.",
                sets="3",
                reps="15 steps each direction",
                focus="Strengthen hip abductors and improve knee tracking"
            ),
            'ankle_mobility': CorrectiveExercise(
                name="Ankle Dorsiflexion Stretch",
                description="Face a wall with one foot forward. Keep heel down and lean forward, feeling stretch in calf and ankle.",
                sets="3",
                reps="30 seconds each side",
                focus="Improve ankle dorsiflexion for better squat depth"
            ),
            'hip_mobility': CorrectiveExercise(
                name="90/90 Hip Stretch",
                description="Sit with one leg at 90° in front, one at 90° to the side. Lean forward over front leg.",
                sets="3",
                reps="45 seconds each side",
                focus="Improve hip internal and external rotation"
            ),
            'core_stability': CorrectiveExercise(
                name="Dead Bug Exercise",
                description="Lie on back, arms up, knees at 90°. Lower opposite arm and leg while maintaining neutral spine.",
                sets="3",
                reps="10 each side",
                focus="Develop core stability and prevent excessive forward lean"
            ),
            'depth_training': CorrectiveExercise(
                name="Goblet Squat",
                description="Hold weight at chest level and squat deep while maintaining upright torso.",
                sets="3",
                reps="12-15",
                focus="Build strength and mobility for proper squat depth"
            ),
            'forward_lean': CorrectiveExercise(
                name="Wall Squats",
                description="Squat facing a wall, staying close without touching it. Forces upright torso position.",
                sets="3",
                reps="10-12",
                focus="Reinforce upright torso positioning"
            ),
            'balance': CorrectiveExercise(
                name="Single-Leg Romanian Deadlift",
                description="Stand on one leg, hinge at hip while extending other leg back for balance.",
                sets="3",
                reps="8-10 each leg",
                focus="Improve balance and unilateral strength"
            )
        }

    def analyze(self, poses: List[Dict]) -> AnalysisResult:
        """Analyze squat form from pose data."""
        issues = []
        recommendations = []
        corrective_exercises = []
        scores = []

        # Find the deepest squat position
        deepest_squat = self._find_deepest_squat(poses)

        if not deepest_squat:
            return AnalysisResult(
                exercise="Squat",
                overall_score=0.0,
                issues=[FormIssue(
                    issue="No squat detected",
                    severity=Severity.CRITICAL,
                    description="Could not detect a squat movement in the video."
                )],
                recommendations=["Ensure the full squat movement is visible in the video"],
                corrective_exercises=[],
                summary="No valid squat movement detected.",
                frame_count=len(poses)
            )

        # Analyze various aspects of squat form
        knee_issues, knee_score = self._analyze_knee_tracking(poses, deepest_squat)
        issues.extend(knee_issues)
        scores.append(knee_score)

        depth_issues, depth_score = self._analyze_depth(deepest_squat)
        issues.extend(depth_issues)
        scores.append(depth_score)

        back_issues, back_score = self._analyze_back_angle(deepest_squat)
        issues.extend(back_issues)
        scores.append(back_score)

        balance_issues, balance_score = self._analyze_balance(poses)
        issues.extend(balance_issues)
        scores.append(balance_score)

        hip_issues, hip_score = self._analyze_hip_hinge(deepest_squat)
        issues.extend(hip_issues)
        scores.append(hip_score)

        # Calculate overall score
        overall_score = np.mean(scores) if scores else 0.0

        # Generate recommendations and corrective exercises
        recommendations = self._generate_recommendations(issues)
        corrective_exercises = self._get_corrective_exercises(issues)

        # Generate summary
        summary = self._generate_summary(overall_score, issues)

        return AnalysisResult(
            exercise="Squat",
            overall_score=round(overall_score, 2),
            issues=issues,
            recommendations=recommendations,
            corrective_exercises=corrective_exercises,
            summary=summary,
            frame_count=len(poses)
        )

    def _find_deepest_squat(self, poses: List[Dict]) -> Dict:
        """Find the frame with the deepest squat position."""
        min_hip_height = float('inf')
        deepest_pose = None

        for pose in poses:
            left_hip = get_landmark(pose, PoseLandmark.LEFT_HIP)
            right_hip = get_landmark(pose, PoseLandmark.RIGHT_HIP)
            avg_hip_y = (left_hip['y'] + right_hip['y']) / 2

            if avg_hip_y > min_hip_height:  # Higher y = lower position
                min_hip_height = avg_hip_y
                deepest_pose = pose

        return deepest_pose

    def _analyze_knee_tracking(self, poses: List[Dict], deepest_squat: Dict) -> tuple:
        """Analyze knee tracking (valgus/varus)."""
        issues = []
        score = 100.0

        pose = deepest_squat
        left_hip = get_landmark(pose, PoseLandmark.LEFT_HIP)
        left_knee = get_landmark(pose, PoseLandmark.LEFT_KNEE)
        left_ankle = get_landmark(pose, PoseLandmark.LEFT_ANKLE)

        right_hip = get_landmark(pose, PoseLandmark.RIGHT_HIP)
        right_knee = get_landmark(pose, PoseLandmark.RIGHT_KNEE)
        right_ankle = get_landmark(pose, PoseLandmark.RIGHT_ANKLE)

        # Check if knees cave inward (knee valgus)
        left_knee_alignment = left_knee['x'] - left_ankle['x']
        right_knee_alignment = right_ankle['x'] - right_knee['x']

        hip_width = abs(left_hip['x'] - right_hip['x'])

        if left_knee_alignment < -0.03 or right_knee_alignment < -0.03:
            severity = Severity.CRITICAL if (left_knee_alignment < -0.05 or right_knee_alignment < -0.05) else Severity.WARNING
            issues.append(FormIssue(
                issue="Knee Valgus (Knees Caving In)",
                severity=severity,
                description="Your knees are collapsing inward during the squat. This puts stress on the knee joints and can lead to injury.",
                timestamp=pose['timestamp'],
                frames=[pose['frame']]
            ))
            score -= 30 if severity == Severity.CRITICAL else 15

        return issues, score

    def _analyze_depth(self, deepest_squat: Dict) -> tuple:
        """Analyze squat depth."""
        issues = []
        score = 100.0

        left_hip = get_landmark(deepest_squat, PoseLandmark.LEFT_HIP)
        left_knee = get_landmark(deepest_squat, PoseLandmark.LEFT_KNEE)
        right_hip = get_landmark(deepest_squat, PoseLandmark.RIGHT_HIP)
        right_knee = get_landmark(deepest_squat, PoseLandmark.RIGHT_KNEE)

        # Calculate hip to knee vertical distance
        avg_hip_y = (left_hip['y'] + right_hip['y']) / 2
        avg_knee_y = (left_knee['y'] + right_knee['y']) / 2

        depth_ratio = avg_hip_y - avg_knee_y

        # Parallel squat: hips at or below knee level (depth_ratio >= 0)
        if depth_ratio < -0.05:
            issues.append(FormIssue(
                issue="Insufficient Depth",
                severity=Severity.WARNING,
                description="Your squat is not reaching parallel depth (hips level with knees). Aim to descend until your hip crease is at least level with the top of your knees.",
                timestamp=deepest_squat['timestamp'],
                frames=[deepest_squat['frame']]
            ))
            score -= 20
        elif depth_ratio >= 0.05:
            issues.append(FormIssue(
                issue="Excellent Depth",
                severity=Severity.INFO,
                description="Great depth! You're achieving below parallel, which maximizes glute and hamstring engagement.",
                timestamp=deepest_squat['timestamp'],
                frames=[deepest_squat['frame']]
            ))

        return issues, score

    def _analyze_back_angle(self, deepest_squat: Dict) -> tuple:
        """Analyze back angle and forward lean."""
        issues = []
        score = 100.0

        left_shoulder = get_landmark(deepest_squat, PoseLandmark.LEFT_SHOULDER)
        left_hip = get_landmark(deepest_squat, PoseLandmark.LEFT_HIP)
        left_knee = get_landmark(deepest_squat, PoseLandmark.LEFT_KNEE)

        # Calculate torso angle
        torso_angle = calculate_angle(
            left_shoulder,
            left_hip,
            left_knee
        )

        # Excessive forward lean (torso too horizontal)
        if torso_angle > 145:
            issues.append(FormIssue(
                issue="Excessive Forward Lean",
                severity=Severity.WARNING,
                description="Your torso is leaning too far forward. This can strain your lower back and reduce quad engagement. Focus on keeping a more upright torso.",
                timestamp=deepest_squat['timestamp'],
                frames=[deepest_squat['frame']]
            ))
            score -= 20

        return issues, score

    def _analyze_balance(self, poses: List[Dict]) -> tuple:
        """Analyze balance and stability throughout the movement."""
        issues = []
        score = 100.0

        # Track center of mass shifts
        horizontal_variance = []

        for pose in poses:
            left_hip = get_landmark(pose, PoseLandmark.LEFT_HIP)
            right_hip = get_landmark(pose, PoseLandmark.RIGHT_HIP)
            center_x = (left_hip['x'] + right_hip['x']) / 2
            horizontal_variance.append(center_x)

        variance = np.var(horizontal_variance)

        if variance > 0.001:
            issues.append(FormIssue(
                issue="Balance Issues",
                severity=Severity.WARNING,
                description="You're showing some lateral sway during the movement. Focus on keeping your weight centered over your midfoot.",
                frames=list(range(len(poses)))
            ))
            score -= 15

        return issues, score

    def _analyze_hip_hinge(self, deepest_squat: Dict) -> tuple:
        """Analyze hip hinge pattern."""
        issues = []
        score = 100.0

        left_hip = get_landmark(deepest_squat, PoseLandmark.LEFT_HIP)
        left_knee = get_landmark(deepest_squat, PoseLandmark.LEFT_KNEE)
        left_ankle = get_landmark(deepest_squat, PoseLandmark.LEFT_ANKLE)

        # Calculate knee angle
        knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        if knee_angle < 70:
            issues.append(FormIssue(
                issue="Excessive Knee Flexion",
                severity=Severity.INFO,
                description="Your knees are traveling very far forward. While not necessarily wrong, ensure you're also hinging at the hips and engaging your posterior chain.",
                timestamp=deepest_squat['timestamp'],
                frames=[deepest_squat['frame']]
            ))

        return issues, score

    def _generate_recommendations(self, issues: List[FormIssue]) -> List[str]:
        """Generate practical recommendations based on detected issues."""
        recommendations = []

        issue_types = {issue.issue for issue in issues}

        if "Knee Valgus (Knees Caving In)" in issue_types:
            recommendations.append("Focus on actively pushing your knees outward throughout the squat. Think 'knees out' as you descend.")
            recommendations.append("Strengthen your hip abductors with exercises like clamshells and lateral band walks.")

        if "Insufficient Depth" in issue_types:
            recommendations.append("Work on ankle and hip mobility to achieve better depth.")
            recommendations.append("Practice with box squats to build confidence at proper depth.")

        if "Excessive Forward Lean" in issue_types:
            recommendations.append("Keep your chest up and core braced. Imagine a string pulling your chest toward the ceiling.")
            recommendations.append("Try front squats or goblet squats to practice maintaining an upright torso.")

        if "Balance Issues" in issue_types:
            recommendations.append("Keep your weight balanced over your midfoot throughout the movement.")
            recommendations.append("Practice tempo squats (3-second descent) to improve control.")

        if not recommendations:
            recommendations.append("Your form is looking good! Continue practicing with proper technique.")

        return recommendations

    def _get_corrective_exercises(self, issues: List[FormIssue]) -> List[CorrectiveExercise]:
        """Get corrective exercises based on detected issues."""
        exercises = []
        issue_types = {issue.issue for issue in issues}

        if "Knee Valgus (Knees Caving In)" in issue_types:
            exercises.append(self.corrective_exercises_db['knee_valgus'])

        if "Insufficient Depth" in issue_types:
            exercises.append(self.corrective_exercises_db['ankle_mobility'])
            exercises.append(self.corrective_exercises_db['hip_mobility'])
            exercises.append(self.corrective_exercises_db['depth_training'])

        if "Excessive Forward Lean" in issue_types:
            exercises.append(self.corrective_exercises_db['core_stability'])
            exercises.append(self.corrective_exercises_db['forward_lean'])

        if "Balance Issues" in issue_types:
            exercises.append(self.corrective_exercises_db['balance'])

        return exercises

    def _generate_summary(self, overall_score: float, issues: List[FormIssue]) -> str:
        """Generate a summary of the analysis."""
        critical_issues = [i for i in issues if i.severity == Severity.CRITICAL]
        warning_issues = [i for i in issues if i.severity == Severity.WARNING]

        if overall_score >= 90:
            summary = "Excellent squat form! "
        elif overall_score >= 75:
            summary = "Good squat form with minor areas for improvement. "
        elif overall_score >= 60:
            summary = "Decent form, but several areas need attention. "
        else:
            summary = "Significant form issues detected that should be addressed. "

        if critical_issues:
            summary += f"Address {len(critical_issues)} critical issue(s) to prevent injury. "

        if warning_issues:
            summary += f"Work on {len(warning_issues)} technique adjustment(s) to optimize your squat."

        return summary
