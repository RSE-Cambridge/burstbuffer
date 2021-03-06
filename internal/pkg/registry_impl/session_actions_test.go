package registry_impl

import (
	"context"
	"errors"
	"github.com/RSE-Cambridge/data-acc/internal/pkg/datamodel"
	"github.com/RSE-Cambridge/data-acc/internal/pkg/mock_registry"
	"github.com/RSE-Cambridge/data-acc/internal/pkg/mock_store"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestSessionActions_SendSessionAction(t *testing.T) {
	// TODO: need way more testing here
	mockCtrl := gomock.NewController(t)
	defer mockCtrl.Finish()
	brickHost := mock_registry.NewMockBrickHostRegistry(mockCtrl)
	keystore := mock_store.NewMockKeystore(mockCtrl)
	actions := sessionActions{brickHostRegistry: brickHost, store: keystore}
	session := datamodel.Session{Name: "foo", PrimaryBrickHost: "host1"}
	brickHost.EXPECT().IsBrickHostAlive(session.PrimaryBrickHost).Return(true, nil)
	keystore.EXPECT().Watch(context.TODO(), gomock.Any(), false).Return(nil)
	fakeErr := errors.New("fake")
	keystore.EXPECT().Create(gomock.Any(), gomock.Any()).Return(int64(3), fakeErr)

	channel, err := actions.SendSessionAction(context.TODO(), datamodel.SessionCreateFilesystem, session)

	assert.Nil(t, channel)
	assert.Equal(t, "unable to send session action due to: fake", err.Error())
}
