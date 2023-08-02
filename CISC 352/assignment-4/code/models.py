import nn


class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        # This line of code will return the dot product of self to be used in
        # the training of the perceptron.
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        # This if statement converts x to a scalar so we can compare it to a float
        # and returns 1 if x is greater than 0 and -1 if less than 0.
        if nn.as_scalar(self.run(x)) >= 0.00:
            return 1
        else:
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        # This section of code trains the perceptron with a batch size of 1.
        batchSize = 1
        acc = False
        # While loop that iterates over the dataset and updates the incorrect values
        # and trains the data until it is all accurate.
        while not acc:
            acc = True
            for x, y in dataset.iterate_once(batchSize):
                if nn.as_scalar(y) != self.get_prediction(x):
                    nn.Parameter.update(self.w, x, nn.as_scalar(y))
                    acc = False
                else:
                    continue


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        # Initialize needed parameters
        self.batchSize = 1  # Batch size
        # The following are trainable parameters for different sizes we can use
        # in order to train the network in the proper sized matrix.
        self.parameterOne = nn.Parameter(1, 100)
        self.parameterTwo = nn.Parameter(1, 100)
        self.parameterThree = nn.Parameter(100, 1)
        self.parameterFour = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        # Linear transformation on first parameter
        linTrans = nn.Linear(x, self.parameterOne)
        # This rectified linear unit with find all values that are negative and replace with zero.
        rectLin = nn.ReLU(nn.AddBias(linTrans, self.parameterTwo))
        # Now we will matrix multiplication on the paramter three with the non negative values.
        linTransTwo = nn.Linear(rectLin, self.parameterThree)
        # Returns 1x1 node with proper values with the negative ones and nonnegative ones.
        return nn.AddBias(linTransTwo, self.parameterFour)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        # This method returns the loss of the batch.
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        acceptableLoss = False
        # While loop that will makes sure we iterate over the dataset until the loss is less than 0.02.
        while not acceptableLoss:
            # For loop that iterates over the dataset and train the neural network to come close to the sin(x) wave.
            for x, y in dataset.iterate_once(self.batchSize):
                # Get loss function.
                loss = self.get_loss(x, y)
                # This will compute the gradients of loss for each of the parameters.
                grad = nn.gradients(loss,
                                    [self.parameterOne, self.parameterThree, self.parameterTwo, self.parameterFour])

                # Update the values for each parameter based on a learning rate of 0.01.
                self.parameterOne.update(grad[0], -0.01)
                self.parameterThree.update(grad[1], -0.01)
                self.parameterTwo.update(grad[2], -0.01)
                self.parameterFour.update(grad[3], -0.01)

            # This will make the loop stop when the dataset has an acceptable loss.
            if nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))) < 0.02:
                acceptableLoss == True
                break


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        # Initialize batch size and parameters with appropriate sizes for the training.
        self.batchSize = 10
        self.parameterOne = nn.Parameter(784, 100)
        self.parameterTwo = nn.Parameter(1, 100)
        self.parameterThree = nn.Parameter(100, 10)
        self.parameterFour = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        # Linear transformation on first parameter.
        linTransOne = nn.Linear(x, self.parameterOne)
        # This rectified linear unit with find all values that are negative and replace with zero.
        rectLin = nn.ReLU(nn.AddBias(linTransOne, self.parameterTwo))
        # Now we will matrix multiplication on the paramter three with the non negative values.
        linTransTwo = nn.Linear(rectLin, self.parameterThree)
        # Returns 1x1 node with proper values with the negative ones and nonnegative ones.
        return nn.AddBias(linTransTwo, self.parameterFour)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        # This method will return the loss of the batch.
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        accurate = False
        # While loop which will go until the dataset is accurate enough.
        while not accurate:
            # For loop which will iterate over the dataset and update the values in order to train it.
            for x, y in dataset.iterate_once(self.batchSize):
                # Get loss function.
                loss = self.get_loss(x, y)
                # This will compute the gradients of loss for each of the parameters.
                grad = nn.gradients(loss,
                                    [self.parameterOne, self.parameterThree, self.parameterTwo, self.parameterFour])

                # Update the values for each parameter based on a learning rate of 0.01.
                self.parameterOne.update(grad[0], -0.09)
                self.parameterThree.update(grad[1], -0.09)
                self.parameterTwo.update(grad[2], -0.09)
                self.parameterFour.update(grad[3], -0.09)

            # If the dataset is accurate enough break the loop and stop.
            if dataset.get_validation_accuracy() > 0.975:
                accurate == True
                break

