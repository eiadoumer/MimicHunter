class RBNode:
    def __init__(self, score, doc_pair):
        self.score = score          # key (similarity)
        self.pair = doc_pair        # tuple (doc1, doc2)
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1              # 1 = RED, 0 = BLACK


class RedBlackTree:
    def __init__(self):
        self.TNULL = RBNode(0, None)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def insert(self, score, doc_pair):
        node = RBNode(score, doc_pair)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.score < x.score:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.score < y.score:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 0
            return
        if node.parent.parent is None:
            return
        self.fix_insert(node)

    def inorder_reverse(self, node, result):
        if node == self.TNULL:
            return
        self.inorder_reverse(node.right, result)  # calling on node.right instead of node.left  -> Descending order
        result.append((node.pair[0], node.pair[1], node.score))  #  (doc_id_1, doc_id_2, similarity_score)
        self.inorder_reverse(node.left, result)

    def get_sorted_descending(self):
        result = []
        self.inorder_reverse(self.root, result)
        return result

    def display_sorted_pairs(self, threshold_high=0.5, threshold_moderate=0.25):
        pairs = self.get_sorted_descending()
        print(f"{'Rank':<4} {'Pair':<12} {'Score':<8} {'Label'}")
        print("-" * 50)
        rank = 1
        for id1, id2, score in pairs:
            if score >= threshold_high:
                label = "HIGH SIMILARITY"
            elif score >= threshold_moderate:
                label = "MODERATE SIMILARITY"
            else:
                label = "LOW SIMILARITY"
            print(f"{rank:<4} Doc{id1}-Doc{id2:<5} {score:.2f}     {label}")
            rank += 1

    def collect_high_similarity(self, node, result, threshold=0.5):
        if node == self.TNULL:
            return
        self.collect_high_similarity(node.right, result, threshold)

        if node.score >= threshold:  # go left only if node.root.score is >= threshold
            result.append((node.pair[0], node.pair[1], node.score))
            self.collect_high_similarity(node.left, result, threshold)
