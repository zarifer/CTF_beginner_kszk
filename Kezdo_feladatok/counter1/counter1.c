#include <stdint.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

typedef void *universal_f(void *);

typedef struct feature {
    //...
    universal_f *handler;
} feature_t;

static int x = 0;
static char sekrit_x = 0;

static void *sekrit_dokumints(void *_) {
    if (sekrit_x < 0) {
        system("cat flag.txt");
    }
    printf("Come on, this is not a command.\n");
    ++sekrit_x;
    return NULL;
}

static void *hello(void *_) {
    printf("Publicly available commands:\n");
    printf("0 - print this very manual.\n");
    printf("1 - increment the counter.\n");
    printf("2 - check on the counter. Warning: the value will be printed on your screen, do not use this if there are people behind you or your screen is being captured\n");
    printf("3 - exit the software product. Warning: this looses the counter's value permanently.\n");
    return NULL;
}

static void *inc_x(void *_) {
    ++x;
    return NULL;
}

static void *print_x(void *_) {
    printf("Value: %d\n", x);
    return NULL;
}

static void *ex(void *_) {
    exit(0);
}

static void *tusmol(void *_) {
    fprintf(stderr, "Don't be so negative.\n");
}

#define tusmol_feature { tusmol }

struct {
    feature_t hidden_features[10];
    feature_t features[4];
} f = {
    {
        tusmol_feature,
        tusmol_feature,
        tusmol_feature,
        tusmol_feature,
        {
            sekrit_dokumints,
        },
        tusmol_feature,
        tusmol_feature,
        tusmol_feature,
        tusmol_feature,
        tusmol_feature,
    },
    {
        {
            hello,
        },
        {
            inc_x,
        },
        {
            print_x,
        },
        {
            ex,
        },
    },
};

static feature_t *get_feature_by_id(ssize_t id) {
    return f.features + id;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    printf("Welcome to InteractiveCounter 1.0!\n");
    printf("Use command `0` to print the manual.\n");
    while (1) {
        ssize_t id;
        printf("cmd: ");
        if (scanf("%zd", &id) == 1) {
            if (id >= (ssize_t)(sizeof f.features / sizeof (feature_t))) {
                fprintf(stderr, "That's great, invalid command.\n");
            } else if (id < -(ssize_t)sizeof f.hidden_features) {
                tusmol(NULL);
            } else {
                get_feature_by_id(id)->handler(NULL);
            }
        } else {
            if (scanf("%*s") == -1) {
                ex(NULL);
            };
            printf("invalid input\n");
        }
    }
    return 0;
}
