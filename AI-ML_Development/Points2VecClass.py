import numpy as np

class Point2Vec:
    def __init__(self, num_decimals=4):
        self.num_decimals = num_decimals
    
    def truncate(self, number):
        factor = 10 ** self.num_decimals
        return np.round(number * factor) / factor
    
    def normalize(self, value, min_val, max_val):
        """Min-Max normalization"""
        return self.truncate((value - min_val) / (max_val - min_val))
    
    def normalize_vector(self, vector):
        min_val = np.min(vector)
        max_val = np.max(vector)
        normalized_vector = (vector - min_val) / (max_val - min_val)
        return self.truncate(normalized_vector)

    def land2vec(self, landmarks):
        """Convert MediaPipe landmarks to normalized vector representation"""
        vectors = []
        for keyFrame in landmarks:
            vectors.append(
                np.concatenate([
                self.hand2vec(keyFrame[0]),
                self.hand2vec(keyFrame[1]),
                self.pose2vec(keyFrame[2])
                ])
            )
        return vectors

    def hand2vec(self, hand):
        if hand:
            hand_points_vector = np.array([[point.x, point.y, point.z, 1] for point in hand.landmark])
            hand_points_vector[:, 0] = self.normalize_vector(hand_points_vector[:, 0])
            hand_points_vector[:, 1] = self.normalize_vector(hand_points_vector[:, 1])
            hand_points_vector[:, 2] = self.normalize_vector(hand_points_vector[:, 2])
        else:
            hand_points_vector = np.full((21, 4), [-1, -1, -1, 0])
        return hand_points_vector.flatten()

    def pose2vec(self, pose):
        if pose:
            pose_points_vector = np.array([[point.x, point.y, point.z, point.visibility] for point in pose.landmark])
            pose_points_vector[:, 0] = self.normalize_vector(pose_points_vector[:, 0])
            pose_points_vector[:, 1] = self.normalize_vector(pose_points_vector[:, 1])
            pose_points_vector[:, 2] = self.normalize_vector(pose_points_vector[:, 2])
        else:
            pose_points_vector = np.full((33, 4), [-1, -1, -1, 0])
        return pose_points_vector.flatten()
    
    def CNNMaxtrix(self, landmarks):
        vector = self.land2vec(landmarks).flatten()
        returnVector = []
        for keyFrame in vector:
            keyFrame = keyFrame.reshape(15,20)
            zeros_5x20 = np.zeros((5, 20))
            returnVector.append(np.vstack((vector, zeros_5x20)))
        return returnVector